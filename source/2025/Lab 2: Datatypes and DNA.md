# Lab 2: Datatypes and DNA

> # Analyzing DNA

> In this activity, you will implement a datatype on your own. You will have to define and implement all the methods for a datatype that represents a DNA sequence. You will also use the `Set` datatype in this exercise.

+ > ## Background

    >> This section explains some information that is related to this activity. It is for your information only; you do not need to fully understand it to complete the tasks.

    >> Deoxyribonucleic acid (DNA) is a complex biochemical macromolecule that carries genetic information for cellular life forms and some viruses. DNA is also the mechanism through which genetic information from parents is passed on during reproduction. DNA consists of long chains of chemical compounds called nucleotides. Four nucleotides are present in DNA: Adenine (A), Cytosine (C), Guanine (G), and Thymine (T). DNA has a double helix structure containing complementary chains of these four nucleotides connected by hydrogen bonds.

    >> Certain regions of the DNA are called genes. Most genes encode instructions for building proteins (they're called "protein-coding" genes). These proteins are responsible for carrying out most of the life processes of the organism. Nucleotides in a gene are organized into codons. Codons are groups of three nucleotides and are written as the first letters of their nucleotides (e.g., TAC or GGA). Each codon uniquely encodes a single amino acid, a building block of proteins. The process of building proteins from DNA has two major phases called transcription and translation, in which a gene is replicated into an intermediate form called mRNA, which is then processed by a structure called a ribosome to build the chain of amino acids encoded by the codons of the gene.

![SEO-DNA-Images-Codons-2019-01-09-12-12-20.jpeg](Lab%202%3A%20Datatypes%20and%20DNA.assets/SEO-DNA-Images-Codons-2019-01-09-12-12-20.jpeg)

    >> The sequences of DNA that encode proteins occur between a start codon (which we will assume to be ATG) and a stop codon (which is any of TAA, TAG, or TGA). Not all regions of DNA are genes; large portions that do not lie between a valid start and stop codon are called intergenic DNA and have other (possibly unknown) functions. Computational biologists examine large DNA data files to find patterns and important information, such as which regions are genes. Sometimes they are interested in the percentages of mass accounted for by each of the four nucleotide types. Often high percentages of Cytosine (C) and Guanine (G) are indicators of important genetic data.

    >> **More about DNA**: [DNA - Wikipedia](https://en.wikipedia.org/wiki/DNA)

## Programming Exercise

You will implement a datatype called `DNA` that will represent a DNA sequence. This datatype should support the following operations:

    - **creation/constructor**: using a `String` of nucleotide sequences;
    - **isProtein()**: returns `true` if the DNA sequence is a protein and `false` otherwise;
    - **totalMass()**: returns a `double` value that represents the mass of the DNA sequence (this value should be rounded to one digit past the decimal point).
    - **nucleotideCount(char c)**: given a nucleotide (one of `A`, `C`, `G` or `T`), returns the count of that nucleotide in the DNA sequence (and this method returns 0 for all invalid/junk nucleotides).
    - **codonSet()**: returns a `Set` that contains all the distinct codons in the DNA sequence;
    - **mutateCodon(String originalCodon, String newCodon)**: Alters the DNA sequence by replacing all occurrences of `originalCodon` with `newCodon`, and eliminates all junk regions (see details below).
    - **sequence()**: returns the nucleotide sequence.

    For the programming exercise, here are the details that you will need:

    - A nucleotide sequence consists of characters `A`, `C`, `T` and `G`. Other characters can be part of the sequence but we will consider them as representing junk regions. *You may assume that all nucleotides will be represented using the uppercase character.* We will not use `a`, `c`, `g` or `t` as part of the test cases. This is not a major assumption/restriction.
    - A codon is a sequence of three nucleotides. You can ignore junk regions when determining the codons. For example, `ACGT-!BAG` contains two codons: `ACG` and `TAG`.
    - The sequence `ATCGAA` represents the codons `ATC` and `GAA`. Further this sequence has the following nucleotide count: `A: 3`, `C: 1`, `G: 1`, and `T: 1`.
    - To determine the mass of a sequence, we will use the following list for the mass of a nucleotide (in gms/mol).
        - Adenine (A): 135.128
        - Cytosine (C): 111.103
        - Guanine (G): 151.128
        - Thymine (T): 125.107
        - Junk: 100.000
    - **Proteins**: we will assume that a DNA sequence is a protein-coding gene if the following criteria are met.
        - The sequence starts with the codon `ATG`;
        - The sequence ends with one of these codons: `TAA`, `TAG`, `TGA`;
        - Contains at least five codons including the start and stop codons;
        - Cytosine and Guanine account for at least 30% of the total mass of the DNA sequence.
        - For the purpose of determining the starting and ending codon, ignore all junk regions.
    - When you perform a **mutation**, you should also remove all the junk regions. You should verify that the old codon and the new codon are valid codons, otherwise the mutation should have no effect.
    - If you want to round a number to one decimal place, you may want to try something like this:

```java
double y = 3.1412;
double x = Math.round(y * 10.0) / 10.0;
```

    - Every DNA sequence should have complete codons. Your constructor should reject invalid sequences such as `ATCGAxbTTz` that have a few complete codons (`ATC`, `GAT`) but there is a codon that is incomplete. When a string passed to the constructor fails to meet this requirement, an `IllegalArgumentException` must be thrown. You can do this rather easily. An example is here:

```java
// assuming there is a function/method to validate a String
if (!valid(dnaSequence)) {
	throw new IllegalArgumentException("Invalid DNA sequence");
}
```

    - We will discuss exceptions but you can read ahead. Consult the [official Java tutorial](https://docs.oracle.com/javase/tutorial/essential/exceptions/index.html).
    - You will have to work with sets in this exercise. In particular, you will have to return a `Set<String>` for the operation `codonSet`. You can read more about this datatype and a concrete implementation, `HashSet`, as part of the [official Java documentation](https://docs.oracle.com/javase/8/docs/api/java/util/HashSet.html).

## Notes

    - You should implement the `DNA` datatype in the file `DNA.java`, which is in the directory `src/main/java/dna`.
    - You **should not** change the directory structure.
    - The `DNA` datatype is part of the `dna` package. Remember to start the `DNA.java` file with the statement `package dna;`

    Also read: [Creating and Using Packages (The Java™ Tutorials > Learning the Java Language > Packages)](https://docs.oracle.com/javase/tutorial/java/package/packages.html)

> ## Grading

> The programming aspect of this assignment represents the bulk of the grade. You should also answer a few questions on PrairieLearn. (Answering the questions on PrairieLearn correctly will give one extra point.)

- > If you pass all the grading tests then you will receive 8 points (equivalent of a B+).
- > If your implementation fails 1 or 2 tests then you will receive a B (7 points).
- > If your implementation fails 3 or 4 tests then you will receive a C (5 points).
- > If your implementation fails 5 tests then you will receive an F+ (3 points).
- > If your implementation fails more than 5 tests then you will not receive any credit for the programming aspect. (You may still get up to 1 point for the questions on PL.)
