# Raft Consensus Algorithm

Raft is a consensus algorithm designed for **understandability**. It solves the same problem as Paxos — getting a cluster of nodes to agree on a sequence of values — but decomposes the problem into three cleanly separated subproblems: leader election, log replication, and safety.

Published in 2014 by Diego Ongaro and John Ousterhout (Stanford) in the paper [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf).

---

## Why Consensus Matters

In a distributed system, nodes can crash, messages can be lost or delayed, and clocks can drift. Consensus ensures that a group of nodes agrees on the same sequence of operations, even when some nodes fail. Without consensus, you cannot build:

- Replicated state machines (the foundation of fault-tolerant services)
- Distributed databases with strong consistency
- Leader election for coordination services
- Distributed locks and configuration management

**Key guarantee:** if any node believes a value has been committed, then every other functioning node will eventually agree on the same value — even if minority nodes crash.

---

## The Three Subproblems

### 1. Leader Election

Raft uses a **strong leader** model — all client requests go through a single leader, and only the leader replicates log entries to followers.

#### Node Roles

Every node is in one of three states:

```
┌──────────┐     timeout      ┌───────────┐    wins election    ┌──────────┐
│ Follower │ ──────────────►  │ Candidate │  ─────────────────► │  Leader  │
└──────────┘                  └───────────┘                     └──────────┘
     ▲                             │                                  │
     │         loses election      │                                  │
     │         or discovers leader │     discovers higher term        │
     │◄────────────────────────────┘◄─────────────────────────────────┘
```

- **Follower** — passive; responds to RPCs from leaders and candidates
- **Candidate** — actively seeking votes to become leader
- **Leader** — handles all client requests; replicates log entries to followers

#### Terms

Time is divided into **terms** — monotonically increasing integers. Each term begins with an election. Terms act as a logical clock: if a node receives a message with a higher term than its own, it immediately updates its term and reverts to follower.

```
Term 1          Term 2          Term 3          Term 4
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Election │    │ Election │    │ Election │    │ Election │
│ Normal   │    │ (split)  │    │ Normal   │    │ Normal   │
│ operation│    │ No leader│    │ operation│    │ operation│
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

#### Why Step Down on a Higher Term?

This rule is Raft's mechanism for **distributed authority revocation**. In a centralized system you can explicitly revoke a leader's authority (e.g., invalidate a token). In a distributed system you can't — the revocation message itself might get lost. Raft sidesteps this: instead of explicitly telling a stale leader "you're fired," every message carries a term number and every node self-enforces the step-down. Authority is implicitly revoked by the existence of a higher term.

**What goes wrong without it — split brain after a partition heals:**

```
Partition:   [A, B]  |  [C, D, E]

1. A is leader (term 1), gets cut off from the majority
2. C, D, E can't hear heartbeats → C wins election → becomes leader (term 2)
3. Partition heals — A receives a message with term 2
```

Without the step-down rule, A would continue operating as leader of term 1 alongside C leading term 2 — two leaders simultaneously. Clients get conflicting responses and committed entries diverge. With the rule, A sees term 2 > 1, immediately steps down to follower, and accepts C's authority.

The step-down is **immediate** (not "after finishing current operations") because any delay lets the stale leader accept writes it can no longer commit (it has lost its majority), send conflicting `AppendEntries` to followers, and hold open a window where two nodes both believe they are the authority — exactly the state Raft exists to prevent.

#### Election Process

1. A follower's **election timeout** expires (randomized, typically 150–300ms)
2. It increments its term, transitions to candidate, votes for itself
3. It sends `RequestVote` RPCs to all other nodes
4. Each node votes for at most one candidate per term (first-come-first-served)
5. Candidate wins if it receives votes from a **majority** (quorum)
6. If no majority (split vote), a new election starts with a new term

The randomized election timeout is the key mechanism that prevents repeated split votes — different nodes time out at different moments, so one usually starts the election first and wins before others even begin.

### 2. Log Replication

Once a leader is elected, it services client requests. Each request is appended as a new **log entry**.

#### Log Structure

```
Index:    1        2        3        4        5        6
Term:    [1]      [1]      [1]      [2]      [3]      [3]
Command: x←3      y←1      x←9      y←2      x←7      y←5

                                              ▲
                                         commitIndex
```

Each entry contains:
- **Index** — position in the log (monotonically increasing)
- **Term** — the term when the entry was created
- **Command** — the state machine command (e.g., `SET x = 3`)

#### Replication Flow

```
Client ──► Leader
             │
             ├── AppendEntries RPC ──► Follower A  (ack)
             ├── AppendEntries RPC ──► Follower B  (ack)
             ├── AppendEntries RPC ──► Follower C  (ack)
             └── AppendEntries RPC ──► Follower D  (down — no ack)
             
             Majority (3/5) acknowledged
             │
             ▼
           Commit ──► Apply to state machine ──► Reply to client
```

1. Leader appends the entry to its local log
2. Leader sends `AppendEntries` RPCs to all followers in parallel
3. When a **majority** of nodes have stored the entry, the leader considers it **committed**
4. Leader applies the committed entry to its state machine and responds to the client
5. Followers learn about committed entries in subsequent `AppendEntries` RPCs and apply them

#### Log Matching Property

Raft maintains two invariants that keep logs consistent:

1. If two entries in different logs have the same index and term, they store the same command
2. If two entries in different logs have the same index and term, all preceding entries are identical

If a follower's log diverges from the leader's (due to a crash), the leader finds the last point of agreement and overwrites the follower's divergent entries. The leader never overwrites its own log.

### 3. Safety

The critical safety property: **if a leader has committed a log entry, that entry will be present in the logs of all future leaders**.

This is enforced by the **election restriction**: a candidate cannot win an election unless its log is at least as up-to-date as a majority of nodes. "Up-to-date" means: higher last-log term, or same term but longer log. Since the committed entry exists on a majority, and the candidate must get votes from a majority, at least one voter has the committed entry — and that voter will refuse to vote for a candidate with an older log.

---

## Cluster Membership

Raft handles configuration changes (adding/removing nodes) using **joint consensus**:

1. Leader creates a transitional configuration `C_old,new` (union of old and new)
2. Decisions require majorities from **both** the old and new configurations
3. Once `C_old,new` is committed, the leader creates `C_new`
4. Once `C_new` is committed, the old configuration is no longer relevant

This ensures that no single point in time has two independent majorities that could elect different leaders.

---

## Log Compaction — Snapshots

Logs grow without bound. Raft uses **snapshots** to compact the log:

1. Each node independently takes a snapshot of its committed state machine state
2. The snapshot replaces all log entries up to the snapshot's last included index
3. If a follower is too far behind, the leader sends its snapshot via `InstallSnapshot` RPC instead of replaying old log entries

---

## Raft in Practice

| System | How Raft is Used |
|---|---|
| [etcd](https://etcd.io/) | Core consensus — Kubernetes cluster state |
| [Consul](https://www.consul.io/) | Service discovery and configuration |
| [CockroachDB](https://www.cockroachlabs.com/) | Per-range consensus for distributed SQL |
| [TiKV](https://tikv.org/) | Distributed key-value store (PingCAP) |
| [RethinkDB](https://rethinkdb.com/) | Cluster coordination |
| [Hashicorp Nomad](https://www.nomadproject.io/) | Job scheduling consensus |

### Typical Cluster Sizes

| Nodes | Tolerates failures | Use case |
|---|---|---|
| 3 | 1 | Minimum fault-tolerant cluster |
| 5 | 2 | Standard production (etcd, Consul) |
| 7 | 3 | High fault-tolerance (rare — latency tradeoff) |

Always use an **odd number** of nodes. Adding a node increases quorum size but only adds one more failure tolerance at even numbers.

---

## Raft vs Paxos

| | Raft | Paxos |
|---|---|---|
| Design goal | Understandability | Theoretical elegance |
| Leader | Strong leader required | Optional (Multi-Paxos uses one) |
| Log replication | Built-in; entries are ordered | Must be layered on top (Multi-Paxos) |
| Membership changes | Joint consensus (specified) | Not specified in original paper |
| Implementations | Many production systems | Few correct implementations |
| Learning curve | Moderate | Notoriously difficult |

Raft and Paxos provide equivalent safety guarantees. The difference is practical: Raft is easier to implement correctly because it decomposes the problem into understandable pieces.

---

## References

- [In Search of an Understandable Consensus Algorithm (Ongaro & Ousterhout, 2014)](https://raft.github.io/raft.pdf)
- [The Raft Consensus Algorithm — Interactive Visualization](https://raft.github.io/)
- [Raft Refloated: Do We Have Consensus? (2015)](https://www.cl.cam.ac.uk/~ms705/pub/papers/2015-osr-raft.pdf)
- [etcd: How Raft Works](https://etcd.io/docs/v3.5/learning/raft/)
- [Students' Guide to Raft (MIT 6.824)](https://thesquareplanet.com/blog/students-guide-to-raft/)
- [Martin Kleppmann — Designing Data-Intensive Applications, Chapter 9](https://dataintensive.net/)
- [Mastering the Raft Consensus Algorithm: A Comprehensive Tutorial in Distributed Systems](https://www.youtube.com/watch?v=ZyqAbQkpeUo)