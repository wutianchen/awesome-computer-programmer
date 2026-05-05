# KRaft (Kafka Raft)

KRaft is Kafka's built-in consensus protocol for metadata management, replacing Apache ZooKeeper. It is based on the Raft consensus algorithm but adapted to fit Kafka's architecture and replication model. Introduced in KIP-500, production-ready since Kafka 3.3.1, and the sole option since Kafka 4.0 (ZooKeeper fully removed).

- [KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)

---

## Why Replace ZooKeeper?

ZooKeeper was an external dependency that added operational complexity:

| Problem | Detail |
|---|---|
| Separate cluster to deploy and monitor | ZooKeeper requires its own nodes, configs, upgrades, and monitoring |
| Metadata bottleneck | All brokers funneled metadata operations through a single ZooKeeper ensemble |
| Controller failover latency | When the Kafka controller died, the new controller had to reload all metadata from ZooKeeper — for large clusters this took minutes |
| Scaling ceiling | ZooKeeper's write throughput limits the number of partitions a cluster can support (~200k practical limit) |
| Split-brain risk | Two separate consensus systems (ZooKeeper for metadata, ISR for data) with different failure modes |

KRaft eliminates all of these by embedding the metadata consensus directly into Kafka.

---

## Architecture

### Metadata Quorum

KRaft introduces a set of **controller nodes** that form a Raft quorum. One controller is the **active controller** (leader); the rest are **standby controllers** (followers).

```
                    Metadata Quorum (Raft)
                 ┌──────────────────────────┐
                 │  Controller 1 (active)    │
                 │  Controller 2 (standby)   │
                 │  Controller 3 (standby)   │
                 └──────────┬───────────────┘
                            │
              Metadata log replicated via Raft
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ Broker 1 │      │ Broker 2 │      │ Broker 3 │
   └──────────┘      └──────────┘      └──────────┘
         │                  │                  │
    (fetch metadata log tail from active controller)
```

Controllers can be dedicated nodes or run on the same nodes as brokers (combined mode). Production recommendation: dedicated controller nodes.

### Metadata Log

All cluster metadata (topics, partitions, configs, ACLs, broker registrations) is stored as an **append-only log** — the `__cluster_metadata` topic. This is a regular Kafka topic replicated among the controller quorum via Raft.

Every metadata change is a record in this log. Brokers consume the tail of this log to keep their local metadata cache up to date.

### Controller Failover

When the active controller fails:

1. Raft election kicks in — a standby controller with the most up-to-date log wins
2. The new active controller already has the full metadata log in memory
3. Failover completes in **seconds**, not minutes (no need to reload from an external store)

This is the single biggest operational improvement over ZooKeeper.

---

## KRaft vs Raft — Key Differences

KRaft is Raft-adapted, not Raft-verbatim. The differences reflect Kafka's existing design patterns.

| Aspect | Standard Raft | KRaft |
|---|---|---|
| **Log replication direction** | Push-based — leader sends `AppendEntries` RPCs to followers | **Pull-based** — followers (and brokers) **fetch** from the leader, like Kafka's normal replication |
| **Who replicates** | All participants are Raft peers | Controllers are Raft peers; **brokers are observers** — they tail the metadata log but don't vote |
| **Commit semantics** | Leader commits when a majority acknowledges | Same majority rule, but acknowledgment comes via fetch responses rather than RPC replies |
| **Log storage** | Implementation-defined (often in-memory + WAL) | Stored as a **Kafka topic** (`__cluster_metadata`) using Kafka's existing log storage engine |
| **Snapshotting** | Each node independently snapshots its state machine | Periodic **metadata snapshots** stored alongside the log segments; brokers can bootstrap from a snapshot instead of replaying the entire log |
| **Client interaction** | Clients send requests to the leader; leader applies to state machine | Clients (brokers) **fetch** the committed log and apply locally — the active controller doesn't serve reads, brokers read from their own cache |
| **Cluster membership** | Joint consensus (C_old,new → C_new) | Managed through metadata records in the log — controller quorum changes are themselves log entries |
| **Election mechanism** | Randomized election timeout | Similar randomized timeout, but **voters are a fixed quorum subset** — a broker that is not a controller cannot become one |

### Why Pull-Based?

Kafka was already built around the fetch paradigm — partition replicas pull from leaders. KRaft follows the same pattern for consistency:

```
Standard Raft (push):
  Leader ──AppendEntries──► Follower
  Leader ──AppendEntries──► Follower
  
KRaft (pull):
  Follower ──Fetch──► Leader ──response with new entries──► Follower
  Broker   ──Fetch──► Leader ──response with new entries──► Broker
```

This means the same networking code, the same flow control, and the same backpressure mechanisms that Kafka already uses for data replication also handle metadata replication.

### Voters vs Observers

In standard Raft, every node in the cluster is a peer that votes and replicates. KRaft separates the cluster into:

- **Voters** (controller nodes) — participate in Raft elections and log replication; typically 3 or 5 nodes
- **Observers** (broker nodes) — tail the committed metadata log but do not vote; can be hundreds of nodes

This is critical for scalability. A 500-broker Kafka cluster doesn't need 500 Raft participants — only 3–5 controllers form the quorum, keeping consensus lightweight while supporting a large data plane.

```
Standard Raft:
  Node 1 (voter) ◄──► Node 2 (voter) ◄──► Node 3 (voter)
  All nodes are equal peers.

KRaft:
  Controller 1 (voter) ◄──► Controller 2 (voter) ◄──► Controller 3 (voter)
       │                          │                          │
       └─── Broker 1 (observer)   │                          │
       └─── Broker 2 (observer)   └─── Broker 3 (observer)  │
       └─── Broker 4 (observer)                              └─── Broker 5 (observer)
                                                             └─── ...Broker N
```

---

## KRaft vs ZooKeeper — What Changed

| Aspect | ZooKeeper Mode | KRaft Mode |
|---|---|---|
| External dependency | ZooKeeper ensemble required | None — self-contained |
| Metadata storage | ZooKeeper znodes (hierarchical key-value) | Kafka log topic (`__cluster_metadata`) |
| Controller election | Via ZooKeeper ephemeral nodes | Via Raft leader election |
| Controller failover | Slow — reload all metadata from ZK | Fast — new leader already has the log |
| Partition limit | ~200k (ZK write bottleneck) | Millions (log-based, no external bottleneck) |
| Operational complexity | Two systems to deploy, monitor, upgrade | One system |
| Consensus protocol | ZAB (ZooKeeper Atomic Broadcast) | KRaft (Raft-based) |

---

## Important: KRaft Is Only for Metadata

KRaft handles **cluster metadata consensus** only. It does NOT replace Kafka's data replication model.

**Partition data** (the actual messages producers write and consumers read) is still replicated using Kafka's **ISR (In-Sync Replicas)** protocol:

- The partition leader writes to its local log
- Follower replicas fetch from the leader
- A message is committed when all ISR members have replicated it
- ISR membership is tracked as metadata — which is now managed by KRaft

```
┌─────────────────────────────────────────────────┐
│                 KRaft (Raft-based)               │
│                                                  │
│  Manages: topics, partitions, configs, ACLs,     │
│  broker registrations, ISR lists                 │
│  Replicated among: controller quorum (3-5 nodes) │
└──────────────────────┬──────────────────────────┘
                       │
                       │ (metadata about which broker leads which partition)
                       ▼
┌─────────────────────────────────────────────────┐
│              ISR Replication (not Raft)          │
│                                                  │
│  Manages: actual message data per partition       │
│  Replicated among: partition replicas (brokers)  │
│  Commit rule: all ISR members acknowledged       │
└─────────────────────────────────────────────────┘
```

---

## Configuration

### Controller-only nodes (recommended for production)

```properties
process.roles=controller
node.id=1
controller.quorum.voters=1@controller1:9093,2@controller2:9093,3@controller3:9093
```

### Broker-only nodes

```properties
process.roles=broker
node.id=101
controller.quorum.voters=1@controller1:9093,2@controller2:9093,3@controller3:9093
```

### Combined mode (dev/small clusters)

```properties
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093
```

---

## References

- [KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)
- [Apache Kafka KRaft Documentation](https://kafka.apache.org/documentation/#kraft)
- [Apache Kafka Without ZooKeeper — Confluent Blog](https://www.confluent.io/blog/removing-zookeeper-dependency-in-kafka/)
- [KRaft: Apache Kafka Without ZooKeeper — Colin McCabe, Confluent](https://www.youtube.com/watch?v=LN1ByaEBRAM)
- [Kafka 4.0: ZooKeeper Is Gone — Gunnar Morling](https://www.morling.dev/blog/kafka-4-0-zookeeper-is-gone/)
- [In Search of an Understandable Consensus Algorithm (Raft paper)](https://raft.github.io/raft.pdf)
