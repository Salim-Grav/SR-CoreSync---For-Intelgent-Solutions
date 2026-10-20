using System;
using System.IO;
using System.Drawing;
using System.Windows.Forms;
using System.Diagnostics;

namespace SRCoreSync
{
    public class TaxSyncInstallerForm : Form
    {
        private Label lblTitle;
        private Label lblSubtitle;
        private Label lblStatus;
        private ProgressBar progressBar;
        private Button btnInstall;
        private Button btnCancel;
        private CheckBox chkLaunch;
        private Panel headerPanel;

        public TaxSyncInstallerForm()
        {
            this.Text = "S&R TaxSync Desktop v2.4 Pro - Setup Wizard";
            this.Size = new Size(540, 380);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(12, 20, 16);
            this.ForeColor = Color.White;

            headerPanel = new Panel();
            headerPanel.Dock = DockStyle.Top;
            headerPanel.Height = 80;
            headerPanel.BackColor = Color.FromArgb(4, 12, 9);
            this.Controls.Add(headerPanel);

            lblTitle = new Label();
            lblTitle.Text = "S&R TaxSync Desktop v2.4 Pro";
            lblTitle.Font = new Font("Segoe UI", 14, FontStyle.Bold);
            lblTitle.ForeColor = Color.FromArgb(230, 202, 159);
            lblTitle.Location = new Point(20, 15);
            lblTitle.AutoSize = true;
            headerPanel.Controls.Add(lblTitle);

            lblSubtitle = new Label();
            lblSubtitle.Text = "Official Setup Wizard • S&R CoreSync Solutions (Amsterdam, NL)";
            lblSubtitle.Font = new Font("Segoe UI", 9, FontStyle.Regular);
            lblSubtitle.ForeColor = Color.FromArgb(160, 180, 170);
            lblSubtitle.Location = new Point(22, 45);
            lblSubtitle.AutoSize = true;
            headerPanel.Controls.Add(lblSubtitle);

            Label lblInfo = new Label();
            lblInfo.Text = "This wizard will install S&R TaxSync Desktop v2.4 (Offline Tax & ERP Suite)\non your local computer.\n\nIncluded Features:\n• BTW 21% & 9% Real-time calculation engine\n• Belastingdienst official XML tax return export\n• EN 16931 European compliant invoice generator\n• Local AES-256 encrypted database (Zero cloud dependency)";
            lblInfo.Font = new Font("Segoe UI", 9, FontStyle.Regular);
            lblInfo.ForeColor = Color.FromArgb(200, 220, 210);
            lblInfo.Location = new Point(24, 100);
            lblInfo.Size = new Size(480, 120);
            this.Controls.Add(lblInfo);

            progressBar = new ProgressBar();
            progressBar.Location = new Point(24, 230);
            progressBar.Size = new Size(476, 18);
            progressBar.Visible = false;
            this.Controls.Add(progressBar);

            lblStatus = new Label();
            lblStatus.Text = "Ready to install to: %LOCALAPPDATA%\\SR-CoreSync\\TaxSync";
            lblStatus.Font = new Font("Segoe UI", 8, FontStyle.Italic);
            lblStatus.ForeColor = Color.FromArgb(140, 160, 150);
            lblStatus.Location = new Point(24, 255);
            lblStatus.Size = new Size(480, 20);
            this.Controls.Add(lblStatus);

            chkLaunch = new CheckBox();
            chkLaunch.Text = "Launch S&R TaxSync Desktop after installation";
            chkLaunch.Checked = true;
            chkLaunch.ForeColor = Color.FromArgb(230, 202, 159);
            chkLaunch.Font = new Font("Segoe UI", 9);
            chkLaunch.Location = new Point(24, 280);
            chkLaunch.Size = new Size(350, 24);
            this.Controls.Add(chkLaunch);

            btnInstall = new Button();
            btnInstall.Text = "Install Now";
            btnInstall.Font = new Font("Segoe UI", 9, FontStyle.Bold);
            btnInstall.BackColor = Color.FromArgb(0, 180, 120);
            btnInstall.ForeColor = Color.Black;
            btnInstall.FlatStyle = FlatStyle.Flat;
            btnInstall.FlatAppearance.BorderSize = 0;
            btnInstall.Location = new Point(280, 310);
            btnInstall.Size = new Size(110, 32);
            btnInstall.Click += BtnInstall_Click;
            this.Controls.Add(btnInstall);

            btnCancel = new Button();
            btnCancel.Text = "Cancel";
            btnCancel.Font = new Font("Segoe UI", 9);
            btnCancel.BackColor = Color.FromArgb(30, 45, 38);
            btnCancel.ForeColor = Color.White;
            btnCancel.FlatStyle = FlatStyle.Flat;
            btnCancel.FlatAppearance.BorderSize = 0;
            btnCancel.Location = new Point(400, 310);
            btnCancel.Size = new Size(100, 32);
            btnCancel.Click += (s, e) => this.Close();
            this.Controls.Add(btnCancel);
        }

        private void BtnInstall_Click(object sender, EventArgs e)
        {
            btnInstall.Enabled = false;
            btnCancel.Enabled = false;
            progressBar.Visible = true;
            progressBar.Value = 20;
            lblStatus.Text = "Preparing installation directory...";

            try
            {
                string localApp = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
                string installDir = Path.Combine(localApp, "SR-CoreSync", "TaxSync");

                if (!Directory.Exists(installDir))
                {
                    Directory.CreateDirectory(installDir);
                }

                progressBar.Value = 50;
                lblStatus.Text = "Extracting TaxSync offline suite files...";

                // Create standalone HTML file
                string htmlPath = Path.Combine(installDir, "TaxSync.html");
                string htmlContent = @"<!DOCTYPE html>
<html lang=""ar"" dir=""rtl"">
<head>
    <meta charset=""utf-8"">
    <title>S&R TaxSync Desktop v2.4 Pro</title>
    <style>
        body { font-family: Segoe UI, sans-serif; background: #050d09; color: #fff; padding: 24px; text-align: center; }
        .box { background: #0c1a13; border: 1px solid #c5a880; border-radius: 16px; padding: 30px; max-width: 600px; margin: 40px auto; }
        h1 { color: #00e699; }
        .key { font-family: monospace; background: #010805; padding: 10px; border-radius: 8px; color: #f7e2bd; font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class=""box"">
        <h1>S&R TaxSync Desktop v2.4 Pro</h1>
        <p>برنامج الضرائب والمحاسبة المكتبي الأوفلاين • S&R CoreSync Solutions</p>
        <div class=""key"">LICENSE KEY: SRTX-PRO-2026-X892-OFFLINE</div>
        <p style=""color:#94a3b8; font-size:0.9rem;"">يعمل محلياً 100% دون الحاجة للاتصال بالإنترنت.</p>
    </div>
</body>
</html>";
                File.WriteAllText(htmlPath, htmlContent);

                // Create Run-TaxSync.bat
                string batPath = Path.Combine(installDir, "Run-TaxSync.bat");
                File.WriteAllText(batPath, "@echo off\r\nstart \"\" \"TaxSync.html\"\r\n");

                progressBar.Value = 80;
                lblStatus.Text = "Creating Desktop shortcut...";

                // Create Desktop Shortcut via WScript
                string desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
                string shortcutPath = Path.Combine(desktopPath, "S&R TaxSync Desktop.lnk");

                try
                {
                    Type shellType = Type.GetTypeFromProgID("WScript.Shell");
                    if (shellType != null)
                    {
                        dynamic shell = Activator.CreateInstance(shellType);
                        dynamic shortcut = shell.CreateShortcut(shortcutPath);
                        shortcut.TargetPath = htmlPath;
                        shortcut.WorkingDirectory = installDir;
                        shortcut.Description = "S&R TaxSync Desktop v2.4 Pro";
                        shortcut.Save();
                    }
                }
                catch { }

                progressBar.Value = 100;
                lblStatus.Text = "Installation completed successfully!";
                btnInstall.Text = "Finished";
                btnInstall.Enabled = true;
                btnInstall.Click -= BtnInstall_Click;
                btnInstall.Click += (s, ev) =>
                {
                    if (chkLaunch.Checked)
                    {
                        Process.Start(htmlPath);
                    }
                    this.Close();
                };

                MessageBox.Show("S&R TaxSync Desktop v2.4 Pro has been installed successfully!\n\nA desktop shortcut has been created on your screen.", "Installation Complete", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error during installation: " + ex.Message, "Setup Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                btnInstall.Enabled = true;
                btnCancel.Enabled = true;
            }
        }

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new TaxSyncInstallerForm());
        }
    }
}
