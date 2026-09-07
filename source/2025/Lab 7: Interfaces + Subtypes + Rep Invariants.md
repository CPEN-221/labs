# Lab 7: Interfaces + Subtypes + Rep Invariants

## Overview

You will continue to work with the same framework from the previous two labs: that of the `JobManager`. In this activity, we will enhance the system by adding functionality to the robots. Each robot now maintains the set of jobs it is assigned to complete. Each job is also augmented with additional information: an execution time and a deadline. The execution time for a job is the time needed by a robot to complete the job; the deadline is the time by which the job must be completed. We will assume that all jobs are ready to execute at time $t = 0$. When a robot is asked to complete all the jobs assigned to it, the robot could use, for now, one of two scheduling policies to sequence the jobs; the two policies are shortest job first and earliest deadline first. When a robot completes jobs assigned to it then it also produces some statistics on job completions.

---

> ## Learning Goals

> This activity focuses on:

- > **Interfaces**: You will see how interfaces are used to define the basic operations that a data type can perform, and how multiple implementations of the same interface are used. You will be able to implement an implementation that conforms to an interface. If the interface defines a type `T` and we have two classes, `S1` and `S2`, which implement the interface `T` then `S1` and `S2` are subtypes of `T`.
- > **Abstract Classes**: When we have more than one implementation of an interface, we may occasionally see the need to share code between the implementations. In Java, we could achieve this by defining an abstract class that implements some of the shared code. We **cannot** create instances of an abstract class. You will **extend** an abstract class and implement a concrete class that can be instantiated.
- > **The `Record` Feature**: A recent addition to Java are `Record` classes that simplify the creation and use of immutable types. You will use `Record` classes to represent, for instance, the `Job` type.
- > **Comparators**: We often find the need to provide a function as an input to another function. One of the most common such use-cases is in **sorting** routines, where we want to invoke a sort function and provide it with another function that can be used by the sort function to determine the order between pairs of items. You will implement a comparator to achieve a desired sorting order.
- > **Representation Invariants**: We will emphasize, once again, the use of representation invariants to develop robust data types.

---

## Interfaces

We have defined the `Robot` type as an `interface`. In Java (and other languages), this feature allows us to simply indicate what are the operations that are permitted for this type. (Of late, [we can do more with interfaces](https://www.baeldung.com/java-interfaces) but originally one could not include **any** implementation as part of an interface. Recent changes are more syntactic sugar and improve productivity, but are not strictly necessary.)

The `Robot` interface permits the following operations:

- `isNull`: checks if a `Robot` is a null robot or not;
- `getId`: obtain a `Robot`‘s id;
- `assignJob`: assign a job to a `Robot`;
- `removeJob`: remove a job from a `Robot`;
- `getJobs`: obtain the set of jobs currently assigned to a `Robot`;
- `completeJobs`: complete the jobs assigned to a `Robot` and obtain some scheduler statistics.

An `interface` allows us to define what operations must be supported but these operations must be **implemented** by a concrete class for us to be able to instantiate values of this type.

In our case, we want to define two types of `Robot`s: an `SJFRobot` that completes jobs in shortest-job-first order and an `EDFRobot` that completes jobs in earliest-deadline-first order. We would say that these two types implement the `Robot` interface. A `List<Robot>` could contain instances of `SJFRobot`s and `EDFRobot`s.

---

## Abstract Classes

We want to implement the two `Robot` types (we can implement even more if we wanted to). **But**, at the least, we would likely have identical implementations of the `getId` method in both implementations. We would like to avoid implementing an identical method (DRY principle) in both `SJFRobot` and `EDFRobot`. To achieve this, we can create an abstract class that implements the `Robot` interface and provides an implementation of, say, `getId`.

We define the `AbstractRobot` class that is an `abstract class` in Java. The `AbstractRobot` class implements the `Robot` interface so it is intended to be a subtype of `Robot`. Our implementation of `AbstractRobot`, principally has a constructor that allows us to set the `Robot`‘s id and the `getId` method.

Because our `AbstractRobot` is an `abstract class`, we do not have to implement every operation in the `Robot` interface. Any concrete class implementing the `Robot` interface must support all the operations in that interface.

We can now **extend** `AbstractRobot` to implement `SJFRobot` and `EDFRobot`. (You have been given the implementation of `SJFRobot` and you must implement `EDFRobot`.) We can extend `AbstractRobot` to define a new `abstract class` or a concrete `class`.

We can only create instances of concrete `class`es. Using the `new` operator with an `abstract class` or an `interface` is a syntax error that is identified by the compiler. In our code base:

```java
Robot r1 = new Robot(1); // syntax error
Robot r2 = new AbstractRobot(2); // syntax error
Robot r3 = new SJFRobot(3); // correct
```

Java’s recent support for default implementation in an `interface` has reduced the need for `abstract class`es in some situations.

Our `AbstractRobot` class also includes definitions of `equals` and `hashCode`. We do so because we have chosen to define equality for `Robot`‘s on the basis of their id alone, and this can be defined using the `abstract class`. We have also indicated that these two methods are `final`: this means that `class`es that extend `AbstractRobot` are not allow to override this implementation with their own.

Our `AbstractRobot` does have a representation and is capable of most of the work we need of our `Robot` implementation. The only specialization we need is for a concrete `Robot` implementation to define the priority rule for job scheduling.

Because `AbstractRobot` has no default constructor (a **default constructor** is a constructor that takes no arguments), any `class` that extends `AbstractRobot` must invoke the constructor for `AbstractRobot` and this is done using the `super` keyword. See the implementation of `SJFRobot`.

A concrete class that implements an `interface` **must** implement all the methods specified in the interface unless a default implementation is provided. An `abstract class` that implements an `interface` may not implement all the methods specified in the `interface`; the methods not implemented in an `abstract class` must be implemented by the concrete `class` that extends the `abstract class`. After all, a concrete `class` that implements an `interface` should support **all the operations specified in the `interface`**.

> In Java, a `class` may only extend one other class but a `class` may implement more than one `interface`. (Other languages do this -- *multiple inheritance* -- differently.) What happens if a `class` were to `implement` two `interface`s, each with a method `f` and identical signatures? You can read the Java documentation for such situations if you are interested but such conflicts are best avoided (they are often the result of poor design choices earlier).

---

## Record Classes

We have implemented the `Job` and `SchedulerStats` types as [`record` classes](https://docs.oracle.com/en/java/javase/17/language/records.html). Let us look at the implementation of the `Job` type:

```java
/**
 * An immutable representation of a job.
 * A job is characterized by a unique identifier,
 * an execution time (time needed to complete the job),
 * and a deadline (the time by which the job must be finished).
 * @param jobId the job's identifier, {@code jobId} > 0
 * @param deadline the job's deadline, {@code deadline} >= 0
 * @param executionTime the job's execution time, {@code executionTime} >= 0
 */
public record Job(int jobId, int deadline, int executionTime) {

    /**
     * Obtain a null job, which can be used as a sentinel.
     * A null job has an identifier of 0.
     * @return a null job
     */
    public static Job getNullJob() {
        return new Job(0, 0, 0);
    }
}
```

A `Job` includes a `jobId`, a `deadline` and an `executionTime`. Notice how we do not have to use the keyword `class` or declare the instance variables. By using a `record` class, we simply define the signature for the constructor and the Java compiler automatically uses the parameters for the constructor to define the representation. The Java compiler also adds some of the basic observer methods: `jobId()` to obtain the job id, `deadline()` to obtain the deadline and `executionTime()` to obtain the execution time of the job. We can add some other methods if we need them (like we have done with `getNullJob()`.)

Record classes eliminate the need to write some of the obvious boilerplate code for getters when we want an immutable type implementation.

---

## Comparators

In our implementation of the different `Robot` types, we want to be able to sort jobs based on different aspects of a job. If we look at the implementation of `AbstractRobot`, we have chosen to represent the set of jobs using a `TreeSet`. A `TreeSet` is called so because the elements of the set are stored using a **binary search tree**, which keeps items in sorted order. We would like to keep the jobs sorted using the execution time. To do so, when we create an instance of `TreeSet`, we would like to provide it with a function that can be used to compare two jobs.

What we want is to pass a method `compare(Job j1, Job j2)` that can be used to order jobs `j1` and `j2`. If `compare(j1, j2)` returns `0` then the two jobs are considered equal. If `compare(j1, j2)` returns a value less (greater) than 0 then `j1` is considered smaller (greater) than `j2`. Java does not allow us to directly pass a function as a parameter to the `TreeSet` constructor. (Other languages permit us to pass functions directly to other functions.) In Java, we have to wrap all such ideas within an instance of a class.

To help us achieve this, Java defines a parameterized `Comparator` interface. This interface has an operation `compare` that we need to define. Because we want to compare two instances of `Job`, the corresponding interface we want to implement is `Comparator<Job>`. When we implement this interface, we can define the `compare` operation.

For `SJFRobot`, we want the following implementation:

```java
class SJFJobComparator implements Comparator<Job> {
 public int compare(Job job1, Job job2) {
            int gap = job1.executionTime() - job2.executionTime();
            if (gap != 0) {
                return gap;
            }
            else {
                return job1.jobId() - job2.jobId();
            }
        }
}
```

The `compare` method uses the execution times of the two jobs; in the case that two jobs have the same execution time then we use the job ids to compare the jobs. (By tie-breaking this way, we can store multiple objects in a `TreeSet` that may have the same execution time without the `TreeSet` implementation thinking that the two jobs are identical and replacing one with another when we add jobs to the set.)

Now, we can create an instance of `TreeSet` as follows:

```java
SJFJobComparator sjfComparator = new SJFComparator();
TreeSet<Job> jobSet = new TreeSet<>(sjfComparator);
```

We abbreviate these three steps into one step in the skeleton code and pass the comparator as a priority rule to the `AbstractRobot` constructor.

```java
new Comparator<Job>() {
        @Override
        public int compare(Job job1, Job job2) {
            int gap = job1.executionTime() - job2.executionTime();
            if (gap != 0) {
                return gap;
            }
            else {
                return job1.jobId() - job2.jobId();
            }
        }
    });
```

> The `Comparator` interface is an example of a **functional interface**: an interface with exactly one operation that is used primarily to pass functions as arguments to other functions.

---

> ## Task

1. > **Start by implementing `EDFRobot`**. Understand the type hierarchy of `Robot` ← `AbstractRobot` ← `EDFRobot`.
2. > After you have implemented `EDFRobot`, you can run the provided tests. You will see that several tests fail. **Begin with `testSJFRobot`. What is the failure?** Debug the implementation to fix this problem. The bug here does not have to do with subtyping. We have three jobs, with execution times 5, 5 and 15, respectively. Per SJF order, we would schedule the first job with execution time 5 and it would finish at $t=5$ for a completion time of $5$. The second job with execution time 5 would finish at $t=10$. The job with execution time 15 will finish at $t=25$. The average completion time is $\frac{5+10+25}{3}$.
3. > After fixing the first bug, **verify that your implementation of `EDFRobot` is also correct.**
4. > Then look at the **failure of `testJobManager`**. Why does this test fail? What you should notice is that the test results indicate that 5 jobs were executed when we only had 3 jobs. Now examine the representation of `JobManager`. The representation is different from the earlier representations. You have been given a `checkRep` method. Is it complete? Correct the `checkRep` method and find the bug in the implementation of `JobManager`. Finish this activity by fixing that bug.
5. > **Notice that a `JobManager` can handle `Robot`s of slightly different types**: it can work with a mix of `SJFRobot`s and `EDFRobot`s. At the same time, the code in `JobManager` is not aware of these types of `Robot`s and this is one of the powers of interfaces and subtypes.

---

> ## Grading

> You will submit work on PrairieLearn only. The `JobManager` programming component of this assignment is worth 6 points and the other questions are worth 3 points.
