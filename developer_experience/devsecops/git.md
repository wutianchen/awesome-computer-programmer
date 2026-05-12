# Git

## Git Submodule

* https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407
* https://www.freecodecamp.org/news/how-to-delete-a-git-branch-both-locally-and-remotely/

## Git Subtree

* https://www.youtube.com/watch?v=sC1sfoCo5qY&t=1s

feature branch: https://martinfowler.com/bliki/FeatureBranch.html
Patterns for Managing Source Code Branches: https://martinfowler.com/articles/branching-patterns.html


## Release Management

* https://medium.com/@jameshamann/a-brief-guide-to-semantic-versioning-c6055d87c90e
* https://semver.org/

## Reference

* Why monorepo’s are cool, but probably not for you - Git Series 5 : https://www.youtube.com/watch?v=pSxx-evc8Kw
* Why Google Stores Billions of Lines of Code in a Single Repository: https://www.youtube.com/watch?v=W71BTkUbdqE
* Why Google Stores Billions of Lines of Code in a Single Repository – Google Research: https://research.google/pubs/pub45424/
* Uber Technology Day: Monorepo to Multirepo and Back Again: https://www.youtube.com/watch?v=lV8-1S28ycM
* Git at Google: Making Big Projects (and Everyone Else) Happy, Dave Borowitz - Git Merge 2015 : https://www.youtube.com/watch?v=cY34mr71ky8
* 042 Splitting one Git Repo into Multiple Repos : https://www.youtube.com/watch?v=P5r_jONyuHo
* Matt Walters - Many repos? Monorepo? Meta repo! : https://www.youtube.com/watch?v=NxQVSzjl3x4
* https://codeburst.io/4-git-submodules-alternatives-you-should-know-592095859b0
* Trunk Based Development : https://trunkbaseddevelopment.com/
* Feature Branching is Evil (Thierry de Pauw, Belgium) : https://www.youtube.com/watch?v=h4DM-Wa0aDQ&t=1123s
* Of Death and Dying: A Journey to Trunk Based Development : https://www.youtube.com/watch?v=qJhmqIv6SJk
* Git patterns and anti-patterns for successful developers : Build 2018 : https://www.youtube.com/watch?v=ykZbBD-CmP8
* A successful Git branching model : https://nvie.com/posts/a-successful-git-branching-model/
* Improving your Development Processes with Git Best Practices : https://www.youtube.com/watch?v=ww4xpcvzLHc
* Release Engineering Keynote | Chuck Rossi | Talks at Google: https://www.youtube.com/watch?v=Nffzkkdq7GM
* 10 Principles of Modern Release Management : https://www.youtube.com/watch?v=5snHXSw4faY

## Concepts

* detached head

Detached head means you are no longer on a branch, you have checked out a single commit in the history (in this case the commit previous to HEAD, i.e. HEAD^)
https://stackoverflow.com/questions/10228760/how-do-i-fix-a-git-detached-head



## Code Snippets

#### Temporarily switch to a different commit

https://stackoverflow.com/questions/4114095/how-do-i-revert-a-git-repository-to-a-previous-commit

If you want to temporarily go back to it, fool around, then come back to where you are, all you have to do is check out the desired commit:

```bash
# This will detach your HEAD, that is, leave you with no branch checked out:
git checkout 0d1d7fc32
```

Or if you want to make commits while you're there, go ahead and make a new branch while you're at it:

```bash
git checkout -b old-state 0d1d7fc32
```

To go back to where you were, just check out the branch you were on again. (If you've made changes, as always when switching branches, you'll have to deal with them as appropriate. You could reset to throw them away; you could stash, checkout, stash pop to take them with you; you could commit them to a branch there if you want a branch there.)


#### Hard delete unpublished commits

If, on the other hand, you want to really get rid of everything you've done since then, there are two possibilities. One, if you haven't published any of these commits, simply reset:

```bash
# This will destroy any local modifications.
# Don't do it if you have uncommitted work you want to keep.
git reset --hard 0d1d7fc32

# Alternatively, if there's work to keep:
git stash
git reset --hard 0d1d7fc32
git stash pop
# This saves the modifications, then reapplies that patch after resetting.
# You could get merge conflicts, if you've modified things which were
# changed since the commit you reset to.
```

If you mess up, you've already thrown away your local changes, but you can at least get back to where you were before by resetting again.


#### Undo published commits with new commits

On the other hand, if you've published the work, you probably don't want to reset the branch, since that's effectively rewriting history. In that case, you could indeed revert the commits. With Git, revert has a very specific meaning: create a commit with the reverse patch to cancel it out. This way you don't rewrite any history. (how to rewrite history)

```bash
# This will create three separate revert commits:
git revert a867b4af 25eee4ca 0766c053

# It also takes ranges. This will revert the last two commits:
git revert HEAD~2..HEAD

#Similarly, you can revert a range of commits using commit hashes (non inclusive of first hash):
git revert 0d1d7fc..a867b4a

# Reverting a merge commit
git revert -m 1 <merge_commit_sha>

# To get just one, you could use `rebase -i` to squash them afterwards
# Or, you could do it manually (be sure to do this at top level of the repo)
# get your index and work tree into the desired state, without changing HEAD:
git checkout 0d1d7fc32 .

# Then commit. Be sure and write a good message describing what you just did
git commit
```


######################################

git-credential-help



help to store credential on disk


git config credential.helper store
git push origin master



https://git-scm.com/docs/git-credential-store 





git commit



amend the commit message

git commit --amend -m "change commit message to this"

amend the commit content

git commit --amend

revert without rewrite the history

git revert





git rm



remove a file from all git history https://www.youtube.com/watch?v=Bo-8EfDpKxA 

git filter-branch --index-filter 'git rm --cached --ignore-unmatch README.md' HEAD



it rewrites the commits which include README.md (file to be deleted)

# -d clean untracked directory
# -f clean untracked file
git clean -df



git cherry-pick



When you are working with a team of developers on a medium to large sized project, managing the changes between a number of git branches can become a complex task. Sometimes you don't want to merge a whole branch into another, and only need to pick one or two specific commits. This process is called 'cherry picking'.



https://www.previousnext.com.au/blog/intro-cherry-picking-git 

git cherry-pick is merge behaviour





git reset



https://medium.com/@porteneuve/mastering-git-reset-commit-alchemy-ba3a83bdfddc 





git rebase



difference between git rebase (on top of master) and git merge





git merge



-squash



Squash commits  

 



# 38 here means squash the previous 38 commits
git rebase -i origin/dev~38 dev
git push origin +dev



update from Upstream



git pull = git fetch + git merge FETCH_HEAD



FETCH_HEAD is a short-lived ref, to keep track of what has just been fetched from the remote repository. git pull first invokes git fetch, in normal cases fetching a branch from the remote; FETCH_HEAD points to the tip of this branch (it stores the SHA1 of the commit, just as branches do). git pull then invokes git merge, merging FETCH_HEAD into the current branch. The result is exactly what you'd expect: the commit at the tip of the appropriate remote branch is merged into the commit at the tip of your current branch. This is a bit like doing git fetch without arguments (or git remote update), updating all your remote branches, then running git merge origin/, but using FETCH_HEAD internally instead to refer to whatever single ref was fetched, instead of needing to name things.





git remote



https://stackoverflow.com/questions/9257533/what-is-the-difference-between-origin-and-upstream-on-github 

https://stackoverflow.com/questions/9257533/what-is-the-difference-between-origin-and-upstream-on-github 





git remote rm origin
git remote add origin git@github.com:aplikacjainfo/proj1.git
git config master.remote origin
git config master.merge refs/heads/master



Command

Comment

Scenario

fork

https://help.github.com/en/articles/fork-a-repo

Most commonly, forks are used to either propose changes to someone else's project or to use someone else's project as a starting point for your own idea.

mirror clone

git clone --mirror https://help.github.com/en/articles/duplicating-a-repository

bare clone

git clone --bare

clone

 







git log and git reflog



Visualize branch topology in Git



git log --graph --decorate --oneline



Alternative: gitk





git diff



http://xahlee.info/linux/git_diff.html 







git stash



https://www.atlassian.com/git/tutorials/saving-changes/git-stash 







git config



In Unix systems the end of a line is represented with a line feed (LF). In windows a line is represented with a carriage return (CR) and a line feed (LF) thus (CRLF). when you get code from git that was uploaded from a unix system they will only have an LF.



 

 



Git can handle this by auto-converting CRLF line endings into LF when you add a file to the index, and vice versa when it checks out code onto your filesystem. You can turn on this functionality with the core.autocrlf setting. If you’re on a Windows machine, set it to true – this converts LF endings into CRLF when you check out code:





git config --global core.autocrlf true



If you’re on a Linux or Mac system that uses LF line endings, then you don’t want Git to automatically convert them when you check out files; however, if a file with CRLF endings accidentally gets introduced, then you may want Git to fix it. You can tell Git to convert CRLF to LF on commit but not the other way around by setting core.autocrlf to input:





git config --global core.autocrlf input



This setup should leave you with CRLF endings in Windows checkouts, but LF endings on Mac and Linux systems and in the repository.

‌

If you’re a Windows programmer doing a Windows-only project, then you can turn off this functionality, recording the carriage returns in the repository by setting the config value to false:



git config --global core.autocrlf false



git ls-files