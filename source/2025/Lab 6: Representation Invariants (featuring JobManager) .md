# Lab 6: Representation Invariants (featuring JobManager)

## Overview

In Lab 5, you designed and programmed your own implementation of the `JobManager` abstract data type (ADT). In this lab, you're given a buggy implementation of the `JobManager`, and you're tasked with formulating its representation invariant (RI) and programming this RI in the form of a `checkRep` method, which ensures all conditions of the RI are met.  Using your `checkRep` method, you should find & fix all the bugs in the given implementation. You are **not allowed to change the representation (fields) of the implementation** in any way.

---

> ## The `JobManager` ADT Operations (Same as Lab 5)

> A `JobManager` is seeded with `n` (the number of jobs it is managing). Each of these `n` jobs are initially “unassigned” (i.e., not assigned to a robot). One can then add `Robots`, assign jobs to the `Robots`, and move jobs among the `Robots`.

> The principal operations that the `JobManager` ADT supports are as follows:

- > **Create Instance** `JobManager(int n)` → Create a new `JobManager` instance with `n` jobs with all IDs in `[1, n]`.
- > **Add robot** `addRobot(Robot robot)` → Add a new robot to the pool of robots that can complete jobs.
- > **Check has robot** `hasRobot(Robot robot)` → Check if `robot` exists in the pool of `Robots` maintained.
- > **Remove robot** `removeRobot(Robot)` → Remove a robot from the pool of robots; all jobs assigned to the robot that was removed will be “unassigned”.
- > **Assign jobs** `assignJobs(Robot robot, int jobId)`  → Assign all unassigned jobs with id $\le$ `jobId` to `robot`.
- > **Check if job is assigned** `isAssigned(int jobId)` → Checks if the job with id = `jobId` is assigned to any `Robot` in the pool.
- > **Move some jobs** `moveJobs(Robot srcRobot, dstRobot, int jobId)` → Move all jobs with id $\le$ `jobID` from `srcRobot` to `dstRobot`.
- > **Move all jobs** `moveJobs(Robot srcRobot, dstRobot)` → Move all jobs from `srcRobot` to `dstRobot`.
- > **Get assigned robot** `getRobot(int jobId)` → Identify the `Robot` that is responsible for the job with `jobId` as its id.
- > **Get highest priority job assigned to a robot** `getHighestPriorityJob(Robot robot, int jobId)` → Assuming that the job id indicates priority (higher id ⇒ higher priority), obtain the highest priority job assigned to `robot` with job id $\le$ `jobId`.
- > **Check equality** `equals(Object o)` → checks for equality with another object based on a specified notion of representation equality.
- > **Get hashcode** `hashCode()` → returns a hashcode that obeys the contract with `equals()` and that tries to minimize hash collisions through a `Robot` id-aware hash function.

---

> ## Tasks

> You are tasked with completing the following. You are **not allowed to change the representation (fields) of the provided implementation** in any way.

1. > Implement the `checkRep()` method to throw an `AssertionError` if and only if the representation invariant (RI) for the provided implementation of `JobManager` is violated.
    - >> You **cannot** use the `assert` keyword in `checkRep()`. Instead, you must `throw new AssertionError()` if the representation invariant is violated. Otherwise, you will **not** pass the tests on PrairieLearn.
1. > Run the provided test suite for `checkRep()` in `CheckRepTests.java`
2. > Once you have `checkRep()` working, call `this.checkRep()` before all exit points in other methods like `assignJobs`.
3. > Now, you can use `checkRep()` to help you find bugs in the implementation.
    - >>  **Hint:** Look at which test cases were previously passing but started failing right after you added calls to `checkRep()` in the relevant methods.
1. > Fix all the bugs in the implementation, and ensure you’re passing all provided test cases in `JobManagerTests.java` .
2. > Once you’re confident in your solution, submit your code on PrairieLearn.
3. > Answer the questions in the second part of the lab on PrairieLearn. (Or you can start with this if you like too.)

---

> ## Grading

> You will answer some questions on PrairieLearn and you will submit your implementation to PrairieLearn as well. This programming task is worth 6 points and the other questions on PrairieLearn are worth 3 points.
