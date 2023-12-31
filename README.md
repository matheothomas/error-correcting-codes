# Error-correcting codes

This project has been realised during my two-year CPGE class in France and was part of the "Grandes écoles" competitive exam of 2023 where it received a 17/20 grade.

## Presentation
This project is aimed towards studying the main principles of error-correcting codes through the linear algebra spectrum, and coding a simulation of the Hamming code.

### Documentation
- [MCOT](https://github.com/matheothomas/error-correcting-codes/blob/main/resources/TIPE/mcot.pdf), it introduces the subject and develops the goals of the presentation, it contains a bibliography.
- [Presentation](https://github.com/matheothomas/error-correcting-codes/blob/main/resources/TIPE/presentation.pdf), used as a support during the assessment of the exam.

## Simulation
Made with python, it simulates the emission and reception of a message, while using the **Hamming code** (7,4) principle to avoid some perturbations.

### Steps
1. The input is an alphanumeric message, converted in binary in ASCII.
2. It is then converted in "analogic" (see graphs below), to simulate an over-the-air transmission.
3. Perturbations are applied on this signal [^1].
[^1]: The perturbations used are **bits inversions** and a **white noise** applied to the "analogic" signal.
4. The signal is converted back in binary.
5. The Hamming code principle is applied.
6. The message is converted in alphanumeric characters.

### Usage
The input at line 185 can be replaced with any string.

### Example
Input : "Hello, World !"
```python
Message initial :  Hello, World !
Message converti en binaire :  0100100001100101011011000110110001101111001011000010000001010111011011110111001001101100011001000010000000100001
Message encodé :  0100101100011001101100101010011011011000110110110110001101101101111111001001111000110010011000000001010100111001011011011111110111001001001101101101100011011011001001010010011000000000100110001111
Message perturbé numérique :  0100101000011001101000101010011001011000110111110110001101101101110111001001111001110000011000000001010100101001011011010111110111001000001111101101100011011011001001000010011100000000000110001111
Message corrigé 0100100001100101011011000110110001101111001011000010000001010111011011110111001001101100011001000010000000100001
Message final :  Hello, World !
```

The following images are produced :

![signal_analogique_emis](https://github.com/matheothomas/error-correcting-codes/blob/main/resources/images/signal_analogique_emis.png)

![signal_analogique_recu](https://github.com/matheothomas/error-correcting-codes/blob/main/resources/images/signal_analogique_recu.png)

![transformee_de_fourier](https://github.com/matheothomas/error-correcting-codes/blob/main/resources/images/transformee_de_fourier.png)
