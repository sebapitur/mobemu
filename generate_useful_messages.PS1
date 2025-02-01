$datasets = @(
    'UPB2011', 'UPB2012', 'UPB2015',
    'Haggle-Intel', 'Haggle-Cambridge', 'Haggle-Content', 'Haggle-Infocom2006',
    'NCCU', 'Sigcomm', 'SocialBlueConn', 'StAndrews'
)

foreach ($dataset in $datasets) {
    Start-Job -ScriptBlock {
        cd ~\Documents\facultate\mobemu\
        .venv\Scripts\Activate.ps1
        $env:DATASET = $using:dataset
        python .\filter_useful_messages.py
    }
}