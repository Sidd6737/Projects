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

public partial class Home : System.Web.UI.Page 
{
   SqlConnection con;
   SqlDataReader dr;
    SqlCommand cmd;
    string conn;
    protected   void Page_Load(object sender, EventArgs e)
    {

        display();
     
           //con = new SqlConnection("server=SUTHAHAR-F92F17\\TEST;database=sample;user id=sa;pwd=sukitha");
          
           
    }
    public void display()
    {
        conn = ConfigurationSettings.AppSettings["ConnectionString"];
       con = new SqlConnection(conn);
    }

  
    //USER LOGIN
   

    protected void ImageButton1_Click(object sender, ImageClickEventArgs e)
    {
        if ((TextBox1.Text == "") &&(TextBox2.Text == ""))
        {
            Label1.Text = "Enter Username and Password to Login";
        }
        else
       {
           
           cmd = new SqlCommand("select * from login", con);
           con.Open();
           dr = cmd.ExecuteReader();                
            while (dr.Read ())
            {

                TextBox1.Text =dr["username"].ToString();
               //{
                   
                 // Session["username"] = TextBox1.Text;
                 //  Server.Transfer("media selection.aspx");
                   //TextBox1.Text = "";
                   //TextBox2.Text = "";
                  
               //}
                
               // else 
                //{
//
               //     Label1.Text = "Invalid Username and Password";
              //  }

            }
        }
    }
    

   
}
