using System;
using System.Data;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;
using System.Data.SqlClient;
using System.Net.Mail;
using System.Net;
using System.ComponentModel;
//using System.Text.RegularExpressions;
public partial class _Default : System.Web.UI.Page 
{
    
   
    protected void Page_Load(object sender, EventArgs e)
    {
   


    }
    

    protected void Button1_Click(object sender, EventArgs e)
    {
        lblname.Text = "U R Registered";
        lblname.Visible = true;
       
    }
    
    
    }

    




