Double_Java = {
    "Math.E": "M_E",
    "Math.PI": "M_PI",
    "Math.sqrt": "sqrt",
    "Math.cbrt": "cbrt",
    "Math.pow": "pow",
    "Math.ceil": "ceil",
    "Math.floor": "floor",
    "Math.rint": "rint",
    "Math.log": "log",
    "Math.log10": "log10",
    "Math.log1p": "log1p",
    "Math.exp": "exp",
    "Math.expm1": "expm1",
    "Math.sin": "sin",
    "Math.cos": "cos",
    "Math.tan": "tan",
}
Float_Java = {"scanner.nextFloat": 'scanf("%f", &'}
Long_Java = {"scanner.nextLong": 'scanf("%ld", &'}
Int_Java = {"scanner.nextInt": 'scanf("%d", &'}
Short_Java = {"scanner.nextShort": 'scanf("%hd", &'}
Byte_Java = {"scanner.nextByte": 'scanf(" %c", &'}
String_Java = {"scanner.nextLine": 'scanf("%s", '}

__MAPPER = {
    "System.out.println": "printf",
    "System.out.printf": "printf",
}

INPUT_FUNC = {
    "scanner.nextDouble": ("double", 'scanf("%lf", &'),
    "scanner.nextFloat": ("float", 'scanf("%f", &'),
    "scanner.nextInt": ("int", 'scanf("%d", &'),
}

TYPE_MAPPER = {
    "String": "char*"
}

IGNORE = ["Scanner", "scanner.close"]

MAPPER = {**Double_Java, **__MAPPER}

SUPPORTED_FUNC = ["System.out.println",
                  "System.out.printf", 
                  "Scanner", 
                  "scanner.close", 
                  "Math.abs"]
