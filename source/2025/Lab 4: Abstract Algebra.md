# Lab 4: Abstract Algebra

## Overview

If you are given a set of elements (in this programming assignment, you will work with `String`s) and an operation defined on pairs of elements in the set (you are explicitly given the mapping from a pair of operands to the output of the operation), can you determine some properties of this set and operation? Can you determine if what is provided satisfies the conditions for being an algebraic group?

---

## Background

A **group** is an algebraic entity with a set `G` and a binary operation (an operation that involves two elements from the set), often denoted `*`, that satisfies the following conditions:

1. There exists an `e` in the set G, such that `a * e = a` and `e * a = a`, for all elements `a` in `G`. Such an element `e` is called the **identity** of the group.
2. For all `a` in `G`, there exists some `a'` in `G`, such that `a * a' = e` and `a' * a = e`. In this case, `a'` is the **inverse** of `a` and `a` is the **inverse** of `a'`.
3. For all `a` and `b` and `c` in `G`, `a * (b * c) = (a * b) * c`. This means `*` is **associative**.
4. For all elements `a` and `b` in `G`, `a * b` is in `G`. This means `G` is **closed** under the operation `*`.

Additionally we will say a group `G` is **commutative** if for all elements `a` and `b` in `G`, `a * b = b * a` and `a * b` is also an element in `G`.

We define the n-th **power** of some element `a` in `G` to be `a^n` where `n` is a positive integer and `a^(n+1)` is defined recursively as follows:

- `a^(n+1) = a * a^n`
- `a^1 = a`

We also define the **order** of an element `a` in `G` to be the smallest possible positive integer `m` such that `a^m = e`, where `e` is the **identity** of the group. Note that **order** is only well defined in a group.

---

#### Example

Let `G = { x1, x2, x3 }` and `*` to be defined by the operation table below. Does this set and operation pair represent a group? Is the operation **commutative**? What is the **order** of `x1`?

| **`*`** | **`x1`** | **`x2`** | **`x3`** |
| ------- | -------- | -------- | -------- |
| `x1`    | `x2`     | `x3`     | `x1`     |
| `x2`    | `x3`     | `x1`     | `x2`     |
| `x3`    | `x1`     | `x2`     | `x3`     |

The table above (which is like a *multiplication table*, except that the `x` values need not be integers and the operation need not be multiplication) can be rewritten using the pair of operands (inputs to the operation) and the output:

| **`xi`, `xj`**   | **`xi * xj`** |
| ---------------- | ------------- |
| **operand pair** | **output**    |
| `x1`, `x1`       | `x2`          |
| `x1`, `x2`       | `x3`          |
| `x1`, `x3`       | `x1`          |
| `x2`, `x1`       | `x3`          |
| `x2`, `x2`       | `x1`          |
| `x2`, `x3`       | `x2`          |
| `x3`, `x1`       | `x1`          |
| `x3`, `x2`       | `x2`          |
| `x3`, `x3`       | `x3`          |

To answer the questions posed at the start of this example, we need to check and see if `G` and `*` satisfy the four conditions we mention in the beginning.

1. A quick search allows us to see that `x3` is the **identity** of the group, so `e = x3` as

```other
x1 * x3 = x3 * x1 = x1
x2 * x3 = x3 * x2 = x2
x3 * x3 = x3
```

2. All elements of `G` have their **inverse** as an element of **G**. We know `x3` is the **identity**, and so for any `xi`, the **inverse** of `xi` is some `xj` such that `xi * xj = xj * xi = x3`. In our example we see

```other
x1 * x2 = x2 * x1 = x3 = e
x2 * x1 = x1 * x2 = x3 = e
x3 * x3 = x3 = e
```

3. The operation is **associative** as `xi * (xj * xk) = (xi * xj) * xk` for all `xi, xj, xk` in `G`. Let us confirm this through the following example:

```other
x1 * (x2 * x3) = x1 * x2 = x3
(x1 * x2) * x3 = x3 * x3 = x3
=> x1 * (x2 * x3) = (x1 * x2) * x3
```

4. For each possible pair `xi, xj` in `G`, we see that `xi * xj` is also in `G`. We know this to be true as all entries in the operation table are elements in `G`.

We see that all four conditions of a group hold, therefore `G` and `*` are indeed a group.

The operation is **commutative** as `xi * xj = xj * xi` for any `xi, xj`. We know this to be true as the product table is [symmetric](https://en.wikipedia.org/wiki/Symmetricmatrix).

The **order** of `x1` is **3** as

`x1^3 = x1 * x1^2 = x1 * (x1 * x1) = x1 * x2 = x3 = e`

and **3** is the smallest possible positive integer such that `x1^3 = e`.

---

> ## Your Tasks

> You have to implement the `ProbableGroup` type that is created using a set of elements and an operation on pairs of elements (this operation is described explicitly using a table that maps a pair of values to the output value). In Java vocabulary, the `ProbableGroup` class has a constructor `public ProbableGroup(Set<String> elements, Map<Pair<String>, String) opTable)`.

> Relating to the **background** section, `elements` is our set `G` and `opTable` is our operation table. `opTable` is initialized such that `opTable.get(new Pair("x1","x2"))` returns the result of the operation `x1 * x2`, and `x1`, `x2` are included in `elements`.

> You need to implement the constructor and complete the following methods:

1. > `String product(String a, String b)`: returns as `a * b`.
2. > `String power(String a, int n)`: returns `a^n`.
3. > `String getIdentity()`: returns the identity element of the group.
4. > `int getOrder(String a)`: returns the order of the element `a`.
5. > `String getInverse(String a)`: returns the inverse of the element `a`.
6. > `boolean isGroup()`: Does this `ProbableGroup` instance satisfy all the conditions of a group as defined in the **background** section?
7. > `boolean isCommutative()`: Is the `*` operation commutative?
8. > Make `ProbableGroup` an **immutable** type without removing any methods.
9. > Implement the method `boolean isSubGroup(Set<String> h)` that returns `true` if and only if elements in `h` are a **subgroup** of `this`.

---

Formally, a non-empty subset `S` of a group `G` is a **subgroup** of `G` if:

1. For every element `s` in `S`, `s'` (the **inverse** of `s`) is also in `S`;
2. For every two elements `s` and `t` in `S`, `s * t` is also in `S`.

For instance `S = {x3}` is a subgroup of `G` as defined in our original example.

More detailed specs provided in the skeleton code and we *recommend* that you implement methods in the provided order. You can assume any constraint stated under `@param` or `requires` in the specs is always satisfied. (You do not need to worry about violations of the preconditions.)

You need to think about how to test your work. Some simple tests are shown at the end of this page.

---

> ## Grading

> You will answer some questions on PrairieLearn and you will submit your implementation that fixes the bugs in the provided code.

> You should submit your code on PrairieLearn and via git to GitHub. If you submit your code correctly to GitHub and it matches your PrarieLearn submission then the grade on PrairieLearn for this lab will be unchanged. If you do not submit your work to GitHub correctly then your grade will be lowered by 2 points (the equivalent of a letter grade reduction).

> This programming task is worth 6 points and the other questions on PrairieLearn are worth 3 points.

---

## Some Tests

```java
public class GroupTests {
    /*
     * This method creates a group with the following product table.
     *         x1 	 x2	   x3
     *       -----------------
     *    x1 | x2    x3    x1
     *       |
     *    x2 | x3    x1    x2
     *       |
     *    x3 | x1    x2    x3
     * */
    private ProbableGroup makeGp1() {
        Set<String> elts = new HashSet<String>();
        elts.add("x1");
        elts.add("x2");
        elts.add("x3");

        Map<Pair<String>, String> productMap = new HashMap<Pair<String>, String>();

        productMap.put(new Pair<String>("x1", "x1"), "x2");
        productMap.put(new Pair<String>("x1", "x2"), "x3");
        productMap.put(new Pair<String>("x1", "x3"), "x1");
        productMap.put(new Pair<String>("x2", "x1"), "x3");
        productMap.put(new Pair<String>("x2", "x2"), "x1");
        productMap.put(new Pair<String>("x2", "x3"), "x2");
        productMap.put(new Pair<String>("x3", "x1"), "x1");
        productMap.put(new Pair<String>("x3", "x2"), "x2");
        productMap.put(new Pair<String>("x3", "x3"), "x3");

        ProbableGroup gp1 = new ProbableGroup(elts, productMap);
        return gp1;
    }

    /*
     * This method creates a group with the following product table.
     *
     *        a	  b
     *       -------
     *    a | a   b
     *      |
     *    b | a   a
     * */
    private ProbableGroup makeGp2() {

        Set<String> elts = new HashSet<String>();
        elts.add("a");
        elts.add("b");

        Map<Pair<String>, String> productMap = new HashMap<Pair<String>, String>();

        productMap.put(new Pair<String>("a", "a"), "a");
        productMap.put(new Pair<String>("a", "b"), "b");
        productMap.put(new Pair<String>("b", "a"), "a");
        productMap.put(new Pair<String>("b", "b"), "a");

        ProbableGroup gp2 = new ProbableGroup(elts, productMap);
        return gp2;
    }

    /*
     * This method creates a group with the following product table.
     *         x1	 x2	   x3    x4
     *       -----------------------
     *    x1 | x1    x2    x3    x4
     *       |
     *    x2 | x2    x3    x4    x1
     *       |
     *    x3 | x3    x4    x1    x2
     *       |
     *    x4 | x4    x1    x2    x3
     * */
    private ProbableGroup makeGp3() {

        Set<String> elts = new HashSet<String>();
        elts.add("x1");
        elts.add("x2");
        elts.add("x3");
        elts.add("x4");

        Map<Pair<String>, String> productMap = new HashMap<Pair<String>, String>();

        productMap.put(new Pair<String>("x1", "x1"), "x1");
        productMap.put(new Pair<String>("x1", "x2"), "x2");
        productMap.put(new Pair<String>("x1", "x3"), "x3");
        productMap.put(new Pair<String>("x1", "x4"), "x4");
        productMap.put(new Pair<String>("x2", "x1"), "x2");
        productMap.put(new Pair<String>("x2", "x2"), "x3");
        productMap.put(new Pair<String>("x2", "x3"), "x4");
        productMap.put(new Pair<String>("x2", "x4"), "x1");
        productMap.put(new Pair<String>("x3", "x1"), "x3");
        productMap.put(new Pair<String>("x3", "x2"), "x4");
        productMap.put(new Pair<String>("x3", "x3"), "x1");
        productMap.put(new Pair<String>("x3", "x4"), "x2");
        productMap.put(new Pair<String>("x4", "x1"), "x4");
        productMap.put(new Pair<String>("x4", "x2"), "x1");
        productMap.put(new Pair<String>("x4", "x3"), "x2");
        productMap.put(new Pair<String>("x4", "x4"), "x3");

        ProbableGroup gp3 = new ProbableGroup(elts, productMap);
        return gp3;
    }

    /*
     * This method creates a group with the following product table.
     *
     *        a	  b
     *       -------
     *    a | a   b
     *      |
     *    b | b   b
     * */
    private ProbableGroup makeGp4() {

        Set<String> elts = new HashSet<String>();
        elts.add("a");
        elts.add("b");

        Map<Pair<String>, String> productMap = new HashMap<Pair<String>, String>();

        productMap.put(new Pair<String>("a", "a"), "a");
        productMap.put(new Pair<String>("a", "b"), "b");
        productMap.put(new Pair<String>("b", "a"), "b");
        productMap.put(new Pair<String>("b", "b"), "b");

        ProbableGroup gp4 = new ProbableGroup(elts, productMap);
        return gp4;
    }

    @Test
    public void testProduct1() {
        ProbableGroup gp1 = makeGp1();
        assertEquals("x3", gp1.product("x1", "x2"));
    }

    @Test
    public void testProduct2() {
        ProbableGroup gp1 = makeGp1();
        assertEquals("x2", gp1.product("x3", "x2"));
    }

    @Test
    public void testProduct3() {
        ProbableGroup gp2 = makeGp2();
        assertEquals("b", gp2.product("a", "b"));
    }

    @Test
    public void testIdentity1() {
        ProbableGroup gp1 = makeGp1();
        assertEquals("x3", gp1.getIdentity());
    }

    @Test
    public void testIdentity2() {
        ProbableGroup gp2 = makeGp2();
        assertEquals("", gp2.getIdentity());
    }

    @Test
    public void testInverse1() {
        ProbableGroup gp2 = makeGp2();
        assertEquals("", gp2.getInverse("b"));
    }

    @Test
    public void testInverse2() {
        ProbableGroup gp3 = makeGp3();
        assertEquals("x4", gp3.getInverse("x2"));
    }

    @Test
    public void testPower1() {
        ProbableGroup gp1 = makeGp1();
        assertEquals("x2", gp1.power("x1", 5));
    }

    @Test
    public void testPower2() {
        ProbableGroup gp2 = makeGp2();
        assertEquals("a", gp2.power("b", 10));
    }

    @Test
    public void testOrder1() {
        ProbableGroup gp1 = makeGp1();
        assertEquals(1, gp1.order("x3"));
    }

    @Test
    public void testOrder2() {
        ProbableGroup gp3 = makeGp3();
        assertEquals(4, gp3.order("x2"));
    }

    @Test
    public void testIsGroup1() {
        ProbableGroup gp1 = makeGp1();
        assertTrue(gp1.isGroup());
    }

    @Test
    public void testIsGroup2() {
        ProbableGroup gp3 = makeGp3();
        assertTrue(gp3.isGroup());
    }

    @Test
    public void testIsGroup3() {
        ProbableGroup gp2 = makeGp2();
        assertFalse(gp2.isGroup());
    }

    @Test
    public void testIsCommutative1() {
        ProbableGroup gp1 = makeGp1();
        assertTrue(gp1.isCommutative());
    }

    @Test
    public void testIsCommutative2() {
        ProbableGroup gp2 = makeGp2();
        assertFalse(gp2.isCommutative());
    }

    @Test
    public void testSubGroup(){
        ProbableGroup gp1 = makeGp1();
        Set<String> subGp1 = new HashSet<>();
        subGp1.add("x3");
        Set<String> subGp2 = new HashSet<>();
        subGp2.add("x1");
        assertFalse(gp1.isSubgroup(subGp2));
        assertTrue(gp1.power("x3", 1).equals("x3"));
    }
}
```
