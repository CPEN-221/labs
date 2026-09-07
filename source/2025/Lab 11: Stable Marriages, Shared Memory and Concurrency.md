# Lab 11: Stable Marriages, Shared Memory and Concurrency

## Overview

> In this assignment, you will complete an implementation of an algorithm that uses concurrency with shared memory. From that perspective, the activity is around understanding and navigating the challenges of programming with shared memory and threads that need synchronization. We will use that abstract problem of finding a stable matching in a bipartite graph to develop and reason about an algorithm that has natural concurrency. This abstract question does translate into multiple application use-cases in social settings and in computing systems (e.g., network switches), and there are ethical implications to such algorithms in social contexts.

---

> ## Learning Outcomes

> **Shared Memory Programming**

- > Implement correct multi-threaded programs that rely on shared state.
- > Identify and implement appropriate use of synchronization mechanisms for shared memory programming.

> **The Stable Matching Problem**

- > Define a bipartite graph.
- > Explain the stable matching (marriage) problem and some of its applications.
- > Develop proofs of correctness for algorithms.
- > Analyze algorithms to understand the impact of subtle design decisions.
- > Evaluate and explain ethical concerns when developing algorithms.
- > Evaluate algorithms for potential bias and unfairness, even without data-driven decision-making.

---

## The Stable Matching Problem

The stable matching problem -- or the stable marriage problem -- is a problem that is defined over a bipartite graph.

**What is a bipartite graph?** A graph is bipartite if the vertices (nodes) can be partitioned into two sets, $\mathcal{V}_1$ and $\mathcal{V}_2$, such that any vertex is in exactly one of the two sets (that is the definition of a partition) and there is no edge between two vertices in the same partition. In other words, for any two vertices $u$ and $v$ that are in the same partition there is no edge between $u$ and $v$. In a bipartite graph, edges can only connect vertices in the two partitions.

In the stable matching problem, every vertex has a ranked list of vertices in the other partition that the vertex would like to be matched with. What we want to do is to determine which vertices should be matched.

When we look at algorithms, we usually start by asking the following questions:

- **Does the algorithm terminate?** This is an important question and is not necessarily obvious for certain algorithms. The very general question “Do we know if some arbitrary algorithm $\mathcal{A}$ that we are given terminates?" is what led Turing to formulate [the Halting Problem](https://en.wikipedia.org/wiki/Halting_problem).
- > **If we know an algorithm will terminate then we can ask: “When will it terminate?”** This question is answered as a function of the size of the input. If the input to an algorithm is $n$ **bits** then we would like a function $t(n)$ that represents the time it takes for the algorithm to terminate for an input of size $n$.  (Even here we are hand-waving slightly; we should also consider the size of the program relative to the input. But we leave that concern aside for now.)

Determining $t(n)$ exactly is often hard so we settle for approximations. We are satisfied with determining $T(n)$ such that $t(n) \le kT(n), n > n_0$ for some constants $k$ and $n_0$. If we can find such a $T(n)$, as well as the associated constants, then we say that $t(n) \in O(T(n))$ or that $t(n)$ is asymptotically dominated by $T(n)$. Ideally, we would like $T(n)$ to be such that $k_1T(n) \le t(n) \le k_2T(n)$ for constants $k_1$ and $k_2$, and that would give us a tight approximation of $t(n)$. If such a $T(n)$ exists then we would say that $t(n) \in \Theta(T(n))$.

In the stable matching problem, we have $2n$ participants, and each participant has a list with $n$ entries, and each entry takes $1+\lfloor \lg{n} \rfloor$ bits (alternatively, we could consider the number of bits per entry as a constant such as 4 bytes). This means that an input to an algorithm that solves the stable matching problem, such as the traditional marriage algorithm or TMA, is $2n \times n \times (1+\lfloor \lg{n} \rfloor)$ bits, which can be described as $\Theta(2n^2\lg{n})$ bits. You will see that TMA takes at most $n^2$ "days”, with three phases per day. The first phase involves $n$ messages, the second phase involves processing those $n$ messages and producing $n$ responses, and the third phase is where the $n$ responses are processed.

Because of the message processing, the work per "day" is $\Theta(n)$ and the total work in the TMA is $O(n^3)$. We would say that the **TMA takes quadratic time relative to the number of participants** but is **linear time relative to the input size**. This is the time complexity of an algorithm. (The analysis that we just completed uses the well-known technique of hand-waving, but only for brevity's sake.)
- **Finally, we study other properties of a solution.** With the TMA, some properties are surprising and may not be desirable.  $n_0$

We are also interested, often enough, in how much memory/storage is needed to solve a problem and whether we can say something about the statistical behaviour of an algorithm (what is the average time to completion). For now, it is sufficient to note that if an algorithm needs $\Theta(n)$ bits of storage -- its space complexity — then its running time cannot be smaller than $\Theta(n)$ because we would need to, at the least, read/write those $n$ bits. It is much harder to say something about the average case behaviour of an algorithm because we may not have data to build probability distributions on, say, the size of the input.

> Now explore the following slide deck that illustrates this problem and presents an algorithm to solve the problem. As you step through the slides, focus on how we establish correctness of algorithms. Also reflect on the work that is needed to move from showing that an algorithm is correct to showing that an implementation of the algorithm is correct.
*For students that are taking a course like MATH 220: notice that the proofs are not difficult but they are subtle.*

[CPEN 221 - Stable Marriages](https://docs.google.com/presentation/d/e/2PACX-1vTjVkzAy_WyD-NhlR-MMTZbaFBiRO7LmI_GSVZ9CHAkWpaVl3pyX3v8hhQfYQhioTXdGy6CLM5b_Tim/pub?start=false&loop=false&delayms=3000)

---

## Implementing the Traditional Marriage Algorithm

You will now complete an implementation of the traditional marriage algorithm that produces a stable matching. In this algorithm, we have proposers and proposees, and each of these entities is modelled using a thread of computation. You are given a partial implementation of the algorithm. In the implementation, each “day” (per the slide deck) is called an iteration, and each iteration is divided into three phases (morning, afternoon, evening in the slide deck).

We use a simple interface, an `AppendOnlyMailbox`, to allow the proposers and proposees to send messages to each other.

In any iteration, during the first phase, the proposers send a proposal to one of the proposees. We use a simple model of numeric identifiers, and a proposer simply sends their numeric identifier to the proposee. The proposees should process the offers they receive in the first phase and send a response during the second phase. During the third phase of an iteration, the proposers examine the responses from the proposees and update their status. The provided implementation uses a shared `state` instance, which is an instance of the `ProcessState` type. The proposers and proposees use this shared state information to determine how they make progress.

- You are given the implementation of the `Proposer` type. Treat this implementation as correct (and it is, once you implement the other pieces); you should not change the `Proposer` type. You have the implement the `Proposee` type and you may need to make some changes to the `ProcessState` to avoid race conditions.

Here is the skeleton code for `Proposee` that you can start with:

```java
package cpen221.stablematching;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a proposee in the stable marriage problem.
 */

public class Proposee implements Runnable {
    private Integer id;
    private List<Integer> preferences;
    private Inbox inbox;
    private AppendOnlyMailbox<Integer>[] inboxesForProposers;
    private ProcessState state;
    private Integer currentMatch = null;

    // Representation Invariant:
    // - this.inboxesForProposers.length == preferences.size()
    // - this.inbox is not null

    /**
     * Create an instance of a proposee
     *
     * @param id                  unique identifier for this proposee
     * @param preferences         is not null and contains a permutation of [0, 1, ..., preferences.size() - 1]
     * @param inbox               is not null
     * @param inboxesForProposers does not contain nulls and inboxesForProposers.length == preferences.size()
     * @param state               shared state of the day, is not null
     */
    public Proposee(Integer id,
                    List<Integer> preferences,
                    Inbox inbox,
                    AppendOnlyMailbox<Integer>[] inboxesForProposers,
                    ProcessState state) {
        this.id = id;
        this.preferences = new ArrayList<>(preferences);
        this.inbox = inbox;
        this.inboxesForProposers = inboxesForProposers;
        this.state = state;
    }

    /**
     * Obtain the id of this proposee
     *
     * @return the id of this proposee
     */
    public int getID() {
        return id;
    }

    /**
     * Obtain the current match
     *
     * @return the current match
     * (could be null if the proposee has not received a proposal yet)
     */
    public Integer getCurrentMatch() {
        return currentMatch;
    }

    /**
     * The traditional marriage algorithm
     */
    public void run() {
        // TODO: Implement this method
    }
}
```

- You also need to implement a method that verifies if a given matching is stable or not. (This method is in the `Utils` class.)

---

> ## Main Tasks

> For this assignment, the graded tasks are:

- > Your implementation of a function that verifies if a given matching is stable or not;
- > Your completion of the stable matching algorithm by implementing `Proposee` and making changes to `ProcessState` to ensure correctness.

---

> # Summary

> This assignment challenges you to implement and reason about a concurrent algorithm for solving the **Stable Matching Problem** in a bipartite graph. By completing this task, you will gain practical experience with shared memory programming, synchronization, and multi-threaded systems while applying these concepts to a well-known algorithm, the **Traditional Marriage Algorithm (TMA)**.

> Through this implementation, you will also analyze and ensure algorithmic correctness, stability, and efficiency. The assignment bridges theoretical foundations with practical applications, allowing you to understand both the underlying problem and its real-world significance in domains like computing systems and social decision-making.

---

# Grading

You should submit your work by pushing your code to GitHub.
There is no submission on PrairieLearn.

| **Achievement**                           | **Grade** |
| ----------------------------------------- | --------- |
| Verifying if a matching is stable or not  | 4 / 9     |
| Correct implementation of stable matching | 5 / 9     |
