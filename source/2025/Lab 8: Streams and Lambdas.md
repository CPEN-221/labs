# Lab 8: Streams and Lambdas

## Overview: What Are Java Streams?

> Java `Stream`s are a powerful feature introduced in Java 8 that allows for functional-style operations on collections of data. A `Stream` is a sequence of elements that supports aggregate operations, such as filtering, mapping, and reducing, in a clean and declarative manner.

---

> ## Learning Outcomes

- > **Understand the Basics of Streams**
    - >> Explain the core concepts of Streams, including intermediate and terminal operations.
    - >> Describe the difference between sequential and parallel streams.
- > **Apply Stream Operations to Complex Data Types**
    - >> Implement common Stream operations such as `filter()`, `map()`, `sorted()`, and `collect()` to process collections of custom objects.
    - >> Use `Stream` pipelines to transform, sort, and aggregate data from objects like `TikTokVideo`.
- > **Use Functional Programming Techniques for Data Processing**
    - >> Write concise, declarative code using `Stream`s to solve practical problems, such as ranking videos by engagement and finding the most active uploader.
    - >> Apply functional programming concepts like `reduce()` to accumulate results and implement custom aggregation logic.
- > **Work with `Optional` to Handle Missing Values**
    - >> Use `Optional` to handle cases where data may be absent, avoiding null values.
    - >> Leverage `Optional` in conjunction with `Stream`s for safe and efficient processing, including methods like `ifPresent()` and `orElse()`.
- > **Identify and Correct Common Mistakes in Stream-Based Code**
    - >> Analyze and critique different implementations of `Stream`-based operations, identifying subtle semantic errors that affect correctness (e.g., incorrect sorting logic, misused reduction operations).
    - >> Correctly select and apply Stream operations to achieve the desired results in data processing tasks.
- > **Explain the Benefits and Trade-offs of Stream Processing**
    - >> Discuss the performance implications of using `Stream`s, including lazy evaluation and parallel stream processing.
    - >> Compare traditional imperative programming with functional approaches using `Stream`s, highlighting readability and maintainability benefits.
- > **Implement and Apply Lambda Expressions**
    - >> Write concise and expressive lambda expressions to pass behavior as parameters to methods, such as filtering, transforming, or reducing data. You should be able to utilize functional interfaces like `Predicate<T>`, `Function<T, R>`, and `Consumer<T>` to perform common operations on collections.

---

## Key Characteristics of `Stream`s

1. **Functional**: Streams encourage functional programming. You can process data without modifying the original collection, and operations are defined in terms of transformations on data.
2. **Lazy Evaluation**: Streams are lazily evaluated, meaning operations are not executed until a terminal operation (like `collect()` or `reduce()`) is invoked. This improves performance by avoiding unnecessary calculations.
3. **Parallelizable**: Streams can be processed in parallel with minimal effort by simply calling `parallelStream()` instead of `stream()`. This makes it easier to take advantage of multi-core processors.
4. **Non-Mutating**: Stream operations do not modify the source collection but instead return new collections or values.

---

## The Stream Pipeline

Streams operate in a pipeline of operations. This pipeline consists of:

1. **Source**: The data to be processed (like a `List`, `Set`, or an array).
2. **Intermediate Operations**: Operations that transform or filter the data (like `filter()`, `map()`, `sorted()`). These operations are lazy and return a new stream.
3. **Terminal Operation**: The final operation that triggers the execution of the pipeline and produces a result (like `collect()`, `reduce()`, or `forEach()`).

Here’s a simple example of a `Stream` pipeline:

```java
List<String> words = Arrays.asList("apple", "banana", "cherry", "date", "elderberry");

List<String> result = words.stream()
    .filter(word -> word.length() > 5)
    .sorted()
    .collect(Collectors.toList());

System.out.println(result);  // Outputs: [banana, cherry, elderberry]
```

**In this example:**

- Source: The `List` of words.
- Intermediate Operations: Filtering words with length greater than 5 and then sorting the remaining words.
- Terminal Operation: Collecting the final list.

---

# Types of Stream Operations

- **Intermediate Operations**:

    These operations return a new Stream and can be chained together. They are lazy and don’t perform any actions until a terminal operation is executed. Common intermediate operations include:

| `filter()`    | Filters elements based on a predicate.      |
| ------------- | ------------------------------------------- |
| `map()`       | Transforms elements by applying a function. |
| `sorted()`    | Sorts the stream.                           |
| `distinct()`  | Removes duplicates.                         |

    Example of `map()` and `filter()`:

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> squaredNumbers = numbers.stream()
    .map(n -> n * n)  // Square each number
    .filter(n -> n > 10)  // Keep only numbers greater than 10
    .collect(Collectors.toList());  // Collect the results into a list

System.out.println(squaredNumbers);  // Outputs: [16, 25]
```

- **Terminal Operations**:

    These operations produce a result or a side effect, such as a collection, a single value, or an action on each element. They trigger the execution of the entire pipeline. Common terminal operations include:

| `collect()`    | Gathers elements of the stream into a collection like a `List`, `Set`, or `Map`.       |
| -------------- | -------------------------------------------------------------------------------------- |
| `forEach()`    | Performs an action for each element of the stream.                                     |
| `reduce()`     | Reduces the elements of a stream into a single value (e.g., summing, finding max/min). |
| `count()`      | Counts the number of elements in the stream.                                           |
| `findFirst()`  | Finds the first element of the stream.                                                 |

    **Example of `forEach()`:**

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.stream()
    .forEach(name -> System.out.println("Hello, " + name));
```

---

# Using Streams for Parallel Processing

One of the major advantages of `Stream`s is the ability to easily process data in parallel, leveraging modern multi-core processors. By simply replacing `stream()` with `parallelStream()`, the `Stream` is processed concurrently.

**Example of parallel processing**

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
int sum = numbers.parallelStream()
    .reduce(0, Integer::sum);

System.out.println(sum);
```

In this case, the sum is calculated in parallel, potentially speeding up execution for larger datasets.

---

# Introduction to `Optional`

In functional programming with `Stream`s, it’s common to encounter cases where a value might be absent, such as the result of filtering. Instead of returning null and risking `null` pointer exceptions, Java provides `Optional<T>`, a container that may or may not hold a value.

**Common `Optional` Methods**:

| `isPresent()`          | Checks if a value is present.                            |
| ---------------------- | -------------------------------------------------------- |
| `ifPresent(Consumer)`  | Executes a block of code if a value is present.          |
| `orElse(T other)`      | Returns the value if present, or a default value if not. |
| `map()`                | Transforms the value inside the `Optional`.              |

**Example using `Optional`:**

```java
Optional<String> maybeName = Optional.of("Alice");
maybeName.ifPresent(name -> System.out.println("Hello, " + name));

Optional<String> emptyName = Optional.empty();
System.out.println(emptyName.orElse("Guest"));
```

**Combining `Stream`s and `Optional`**

`Stream`s and `Optional` often work hand-in-hand when filtering or reducing data. For example, you might want to find the first element that matches a condition, and if no match is found, return an `Optional.empty()`.

**Example:**

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
Optional<String> firstMatch = names.stream()
    .filter(name -> name.startsWith("C"))
    .findFirst();

firstMatch.ifPresent(name -> System.out.println("First match: " + name));
```

`Optional` **is not all good**

We wanted to introduce you to Java’s `Optional` type because it exists and you might encounter it in code. *But* it is not all good. Here is a deeper discussion on the `Optional` type:

[Some Comments on Java’s Optional Type](https://ubc-ece.craft.me/cpen221-notes-JavaOptional)

---

# Stream Example with a Complex Object: TikTok Data

Let’s say we have a `TikTokVideo` class that contains fields like `videoId`, `uploader`, `likes`, `shares`, and `comments`. Here’s how we could use `Stream`s to perform operations on a list of `TikTokVideo` objects.

**Example: Sorting TikTok videos by total engagement (likes + shares + comments):**

```java
List<TikTokVideo> rankedByEngagement = videos.stream()
    .sorted(Comparator.comparingInt(video -> video.getLikes() + video.getShares() + video.getComments()).reversed())
    .collect(Collectors.toList());

rankedByEngagement.forEach(video -> {
    int totalEngagement = video.getLikes() + video.getShares() + video.getComments();
    System.out.println("Video ID: " + video.getVideoId() + ", Total Engagement: " + totalEngagement);
});
```

In this example, we:

- Use `stream()` to create a stream of videos.
- Sort the videos by the sum of likes, shares, and comments (engagement).
- Collect the sorted videos into a List.
- Print the total engagement for each video.

**Example: Finding Recent Videos**

```java
 List<TikTokVideo> recentVideos = videos.stream()
            .filter(video -> video.getUploadTime()
            .isAfter(LocalDateTime.now()
            .minusDays(7)))
            .collect(Collectors.toList());
recentVideos.forEach(video ->
            System.out.println("Recent video ID: " + video.getVideoId()
                               + ", Uploaded: " + video.getUploadTime()));
```

**Example: Calculating Total Engagement Across All TikTok Videos**

Let’s say we want to calculate the total engagement (sum of likes, shares, and comments) across all TikTok videos. The `reduce()` operation can help us aggregate this total in a functional and clean way.

Here’s an example:

```java
int totalEngagement = videos.stream()
    .map(video -> video.getLikes() + video.getShares() + video.getComments())
    .reduce(0, Integer::sum);

System.out.println("Total Engagement across all videos: " + totalEngagement);
```

**Example: Finding the Most Active Uploader**

```java
  Optional<Map.Entry<String, Long>> mostActiveUploader = videos.stream()
      .collect(Collectors.groupingBy(TikTokVideo::getUploader, Collectors.counting()))
      .entrySet().stream()
      .max(Map.Entry.comparingByValue());
```

---

# Introduction to Lambdas

Lambda expressions allow you to express instances of functional interfaces (interfaces with a single abstract method) in a more concise way. They provide a shorthand for creating anonymous classes and can make your code much cleaner and easier to read, especially when working with functional programming constructs like Streams.

**Why Use Lambdas?**

Lambdas are particularly useful when you need to pass behavior (like a block of code) as a parameter to a method. Instead of writing verbose inner classes, lambdas allow you to focus on what should be done, without all the boilerplate code around how to structure it.

Consider this common scenario: You want to filter or transform a collection of data. Traditionally, you might create an anonymous class that implements an interface like `Comparator` or `Runnable`. With lambdas, you can achieve the same result with much less code.

---

# Syntax of a Lambda Expression

A lambda expression has three parts:

- Parameter list: Defines the input to the lambda (like a method’s parameter list).
- Arrow operator (->): Separates the parameter list from the body of the lambda.
- Body: Contains the logic to be executed (like the body of a

```java
(parameters) -> expression
```

If there’s only one parameter, you can omit parentheses.

If there’s only one statement in the body, you can omit curly braces.

**Examples**

- Single parameter, single line body

```java
x -> x * x
```

- Multiple parameters, multi-line body

```java
(a, b) -> {
    int result = a + b;
    return result;
}
```

---

# Lambdas in Practice

## Using Lambdas with a Functional Interface

A functional interface is an interface that has exactly one abstract method. Java provides several commonly used functional interfaces, including:

- `Predicate`: Takes a single argument and returns a boolean (used for filtering).
- `Function`: Takes a single argument and returns a result (used for transforming data).
- `Consumer`: Takes a single argument and performs an action without returning a result (used for side effects like printing).

**Examples**

*Filtering a list of integers to find numbers greater than 10*

```java
Predicate<Integer> isGreaterThan10 = x -> x > 10;
```

 *Doubling a number and returning the result*

```java
Function<Integer, Integer> doubleNumber = x -> x * 2;
```

*Printing out each element in a list*

```java
Consumer<String> printString = s -> System.out.println(s);
```

## Using Lambdas with Streams

Lambdas are especially powerful when used with `Stream`s. Streams provide a way to process data declaratively, and lambdas allow you to specify what should be done with the data.

**Example: Using Lambdas with `filter()` and `map()`**

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6);
List<Integer> filteredAndSquared = numbers.stream()
    .filter(x -> x % 2 == 0)  // Keep only even numbers
    .map(x -> x * x)  // Square each remaining number
    .collect(Collectors.toList());

System.out.println(filteredAndSquared);  // Outputs: [4, 16, 36]
```

## Lambdas with Custom Types

Lambdas can also be applied to more complex data types, like objects. For example, imagine a `Person` class with fields like `name` and `age`. You can use a lambda to extract or manipulate the fields of `Person` instances.

**Example: Filtering and Transforming a List of Objects**

```java
List<Person> people = Arrays.asList(
    new Person("Alice", 30),
    new Person("Bob", 20),
    new Person("Charlie", 40)
);

// Filter people older than 25 and extract their names
List<String> names = people.stream()
    .filter(person -> person.getAge() > 25)  // Filter by age
    .map(Person::getName)  // Extract the name
    .collect(Collectors.toList());

System.out.println(names);  // Outputs: [Alice, Charlie]
```

---

# When to Use Lambdas

- Passing Behavior as a Parameter: You can pass lambdas to methods as parameters, making your code more flexible and reusable. Instead of writing a separate class, a lambda lets you pass a small block of logic directly.
- Reducing Boilerplate Code: Lambdas eliminate the need for boilerplate code, such as creating anonymous classes, making your code more concise and easier to read.
- Functional Programming: Lambdas enable functional programming in Java, allowing you to process collections of data with expressive, declarative code.

# More Examples with Lambdas

**Filtering a list of numbers**

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> evenNumbers = numbers.stream()
    .filter(n -> n % 2 == 0)  // Lambda to filter even numbers
    .collect(Collectors.toList());

System.out.println(evenNumbers);  // Outputs: [2, 4]
```

**Transforming data**

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
List<String> upperCaseNames = names.stream()
    .map(name -> name.toUpperCase())  // Lambda to convert each name to uppercase
    .collect(Collectors.toList());

System.out.println(upperCaseNames);  // Outputs: [ALICE, BOB, CHARLIE]
```

---

> # Summary

> Streams enable clean, functional, and efficient processing of collections, reducing the need for verbose loops and conditionals. They make it easier to perform complex operations like filtering, transforming, and reducing data, all while keeping the code concise and readable.

> `Optional` complements `Stream`s by providing a way to handle absent values safely, avoiding null and potential runtime errors.

> Lambdas allow you to write more concise code by eliminating boilerplate associated with anonymous inner classes. With fewer lines of code, there’s less chance of introducing errors, and it’s easier to understand what the code does. Lambdas let you focus on what needs to be done, without the clutter of how the code is structured. Lambdas enable functional programming patterns in Java, allowing you to treat functions as first-class citizens. You can pass behaviour (i.e., a lambda) to a method, store it in variables, or return it from other methods.

> By understanding and mastering these tools, you can write more expressive, maintainable, and efficient Java code.

---

> # Grading

> You will answer questions on PrairieLearn.
