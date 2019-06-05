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
using System.Data.SqlClient;
public partial class Banner : System.Web.UI.Page
{
    SqlConnection con;
    SqlDataReader dr;
    SqlCommand cmd;
    string conn;
    public void display()
    {
        conn = ConfigurationSettings.AppSettings["ConnectionString"];
        con = new SqlConnection(conn);
    }
    protected void Page_Load(object sender, EventArgs e)
    {
    }

}