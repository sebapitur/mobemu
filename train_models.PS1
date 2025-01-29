$models = @('neural', 'rf', 'svm')
$datasets = @(
    'UPB2011', 'UPB2012', 'UPB2015',
    'Haggle-Cambridge', 'Haggle-Content', 'Haggle-Infocom2006', 'Haggle-Intel',
    'NCCU', 'Sigcomm', 'SocialBlueConn', 'StAndrews'
)

foreach ($dataset in $datasets) {
    foreach ($model in $models) {
        Start-Job -ScriptBlock {
            cd C:\Users\seba_\mobemu\
            .venv\Scripts\Activate.ps1
            $env:MODEL = $using:model
            $env:DATASET = $using:dataset
            python train_model.py
        }
    }
}