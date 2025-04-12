



big_string = '''
| 167 |     24     |      Sigcomm       | hit_rate |      rf-UPB2015       |      0.38      |   SPRAY_FOCUS   |       0.33       |         17.66          |
| 201 |     21     |   Haggle-Content   | hit_rate |      rf-UPB2015       |      0.17      |   SPRAY_FOCUS   |       0.15       |         10.69          |
| 210 |     15     | Haggle-Infocom2006 | hit_rate |        rf-NCCU        |      0.33      |   SPRAY_FOCUS   |       0.3        |          8.51          |
| 218 |     3      |        NCCU        | hit_rate |   rf-Haggle-Content   |      0.17      |   SPRAY_FOCUS   |       0.16       |          7.19          |
| 253 |     21     |      UPB2011       | hit_rate |      rf-Sigcomm       |      0.14      |   SPRAY_FOCUS   |       0.13       |          2.76          |
| 274 |     16     |      UPB2012       | hit_rate |      rf-Sigcomm       |      0.32      |   SPRAY_FOCUS   |       0.32       |          0.03          |
'''



lines = big_string.splitlines()

pretty_dict = {
    'rf' : '"random forest"',
    'svm' : '"support vector machine"',
    'neural' : '"retea neuronala"'
}


for line in lines:
    tokens = line.split('|')
    tokens = [token.strip() for token in tokens]
    tokens = tokens[3:-1]

    if not tokens:
        continue

    model_name = tokens[2].split('-')[0]
    training_dataset = tokens[2].split('-')[1]

    print(f"\item Pentru datasetul {tokens[0]}, folosind modelul {pretty_dict[model_name]} antrenat pe setul de date {training_dataset} este cu {tokens[-1]}\% mai eficient, valorile fiind {tokens[3]} < {tokens[5]}")