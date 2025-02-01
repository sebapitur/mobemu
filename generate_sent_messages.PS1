$datasets = @(
    'UPB2011', 'UPB2012', 'UPB2015',
    'Haggle-Intel', 'Haggle-Cambridge', 'Haggle-Content', 'Haggle-Infocom2006',
    'NCCU', 'Sigcomm', 'SocialBlueConn', 'StAndrews'
)

foreach ($dataset in $datasets) {
    Start-Job -ScriptBlock {
        cd ~\Documents\facultate\mobemu\
        $env:TRACE = $using:dataset
        $env:ALGO = "EPIDEMIC"
        $env:OUTPUT_WRITE = "true"
        java -jar .\target\mobemu-1.0-SNAPSHOT-jar-with-dependencies.jar
    }
}