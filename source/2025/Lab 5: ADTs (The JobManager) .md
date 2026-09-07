# Lab 5: ADTs (The `JobManager`)

## Overview

This lab activity focuses on the design and implementation of an abstract data type (ADT) that we shall call `JobManager`. A `JobManager` is responsible to managing a set of jobs, which are identified by integer IDs from `1` to `n`. A `JobManager` also maintains a set of `Robot` objects that are responsible for completing these jobs. The `JobManager` ADT's operations enable its user to manage the set of `Robots` and the assignment of jobs to those`Robots`.

---

> ## Operations

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

> ## Your Task

> Your task is to implement the `JobManager` ADT in Java by implementing all methods corresponding to the Operations outlined above according to their respective specs detailed in the `JobManager` class file. You **cannot** change the spec of any methods, and you **cannot** change the `Robot` class in any way.

---

> ## Grading

> You will answer some questions on PrairieLearn and you will submit your implementation to PrairieLearn and GitHub.

> **For the implementation aspect of this assignment, we will grade your GitHub submission, with more tests than are used on PrairieLearn. But the tests on PrairieLearn should offer some guidance. (And do not worry about the points on PrairieLearn for the programming question; they do not matter.)**

> This programming task is worth 6 points and the other questions on PrairieLearn are worth 3 points.
