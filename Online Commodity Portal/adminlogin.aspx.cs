using System;
using System.Data;
using System.Configuration;
using System.Collections;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;

public partial class Default : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {

    }
    protected void ImageButton1_Click(object sender, ImageClickEventArgs e)
    {
        if ((TextBox1.Text == "") || (TextBox2.Text == ""))
        {
            Label1.Text = "Enter Login Details";
        }
        else if ((TextBox1.Text == "junj") && (TextBox2.Text == "456") || (TextBox1.Text == "admin") && (TextBox2.Text == "ADMIN"))
        {
            Response.Redirect("Online Trading.aspx");
        }
        else
        {
            Label1.Text = "Invalid Username & Password";
        }
    }
}
