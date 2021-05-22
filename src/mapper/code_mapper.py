Double_Java = [
    "scanner.nextDouble",
    "Math.E",
    "Math.PI",
    "Math.sqrt",
    "Math.cbrt",
    "Math.pow",
    "Math.signum",
    "Math.ceil",
    "Math.floor",
    "Math.random",
    "Math.rint",
    "Math.log",
    "Math.log10",
    "Math.log1p",
    "Math.exp",
    "Math.expm1",
    "Math.sin",
    "Math.cos",
    "Math.tan",
]
Float_Java = ["scanner.nextFloat"]
Long_Java = ["scanner.nextLong"]
Int_Java = ["scanner.nextInt", "Math.round"]
Short_Java = ["scanner.nextShort"]
Byte_Java = ["scanner.nextByte"]
String_Java = ["scanner.nextLine"]

MAPPER = {
    "Math.PI": "M_PI",
    "Math.pow": "pow",
    "Math.sqrt": "sqrt",
    "Math.abs": "abs",
    "System.out.println": "println",
    "System.out.printf": "printf",
}

INPUT_FUNC = {
    "scanner.nextDouble": 'scanf("%lf", &',
    "scanner.nextFloat": 'scanf("%f", &',
    "scanner.nextInt": 'scanf("%d", &',
}

TYPE_MAPPER = {
    "String": "char*"
}

IGNORE = ["Scanner", "scanner.close"]
