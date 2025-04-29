namespace Senior_Project_Hub
{
    partial class frmSeniorProjectHub
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.btnLeft = new System.Windows.Forms.Button();
            this.btnRight = new System.Windows.Forms.Button();
            this.btnSelectImage = new System.Windows.Forms.Button();
            this.picMain = new System.Windows.Forms.PictureBox();
            this.txtResult = new System.Windows.Forms.TextBox();
            this.psbStatus = new System.Windows.Forms.ProgressBar();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.btnStart = new System.Windows.Forms.Button();
            this.lblStatus = new System.Windows.Forms.Label();
            this.tmrProgressTracker = new System.Windows.Forms.Timer(this.components);
            this.btnDelete = new System.Windows.Forms.Button();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            ((System.ComponentModel.ISupportInitialize)(this.picMain)).BeginInit();
            this.SuspendLayout();
            // 
            // btnLeft
            // 
            this.btnLeft.Location = new System.Drawing.Point(475, 371);
            this.btnLeft.Name = "btnLeft";
            this.btnLeft.Size = new System.Drawing.Size(75, 23);
            this.btnLeft.TabIndex = 0;
            this.btnLeft.Text = "< Left";
            this.btnLeft.UseVisualStyleBackColor = true;
            this.btnLeft.Visible = false;
            this.btnLeft.Click += new System.EventHandler(this.btnLeft_Click);
            // 
            // btnRight
            // 
            this.btnRight.Location = new System.Drawing.Point(729, 371);
            this.btnRight.Name = "btnRight";
            this.btnRight.Size = new System.Drawing.Size(75, 23);
            this.btnRight.TabIndex = 0;
            this.btnRight.Text = "Right >";
            this.btnRight.UseVisualStyleBackColor = true;
            this.btnRight.Visible = false;
            this.btnRight.Click += new System.EventHandler(this.btnRight_Click);
            // 
            // btnSelectImage
            // 
            this.btnSelectImage.Location = new System.Drawing.Point(556, 363);
            this.btnSelectImage.Name = "btnSelectImage";
            this.btnSelectImage.Size = new System.Drawing.Size(167, 38);
            this.btnSelectImage.TabIndex = 0;
            this.btnSelectImage.Text = "Select Image (PNG)";
            this.btnSelectImage.UseVisualStyleBackColor = true;
            this.btnSelectImage.Click += new System.EventHandler(this.btnSelectImage_Click);
            // 
            // picMain
            // 
            this.picMain.Location = new System.Drawing.Point(84, 51);
            this.picMain.Name = "picMain";
            this.picMain.Size = new System.Drawing.Size(1110, 158);
            this.picMain.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.picMain.TabIndex = 1;
            this.picMain.TabStop = false;
            this.picMain.Visible = false;
            // 
            // txtResult
            // 
            this.txtResult.Location = new System.Drawing.Point(403, 235);
            this.txtResult.Name = "txtResult";
            this.txtResult.Size = new System.Drawing.Size(472, 20);
            this.txtResult.TabIndex = 2;
            this.txtResult.Visible = false;
            this.txtResult.TextChanged += new System.EventHandler(this.txtResult_TextChanged);
            // 
            // psbStatus
            // 
            this.psbStatus.Location = new System.Drawing.Point(475, 291);
            this.psbStatus.Name = "psbStatus";
            this.psbStatus.Size = new System.Drawing.Size(329, 23);
            this.psbStatus.Style = System.Windows.Forms.ProgressBarStyle.Continuous;
            this.psbStatus.TabIndex = 3;
            this.psbStatus.Visible = false;
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // btnStart
            // 
            this.btnStart.Location = new System.Drawing.Point(584, 320);
            this.btnStart.Name = "btnStart";
            this.btnStart.Size = new System.Drawing.Size(110, 37);
            this.btnStart.TabIndex = 4;
            this.btnStart.Text = "Start";
            this.btnStart.UseVisualStyleBackColor = true;
            this.btnStart.Visible = false;
            this.btnStart.Click += new System.EventHandler(this.btnStart_Click);
            // 
            // lblStatus
            // 
            this.lblStatus.AutoSize = true;
            this.lblStatus.Location = new System.Drawing.Point(475, 272);
            this.lblStatus.Name = "lblStatus";
            this.lblStatus.Size = new System.Drawing.Size(0, 13);
            this.lblStatus.TabIndex = 5;
            this.lblStatus.Visible = false;
            // 
            // tmrProgressTracker
            // 
            this.tmrProgressTracker.Tick += new System.EventHandler(this.tmrProgressTracker_Tick);
            // 
            // btnDelete
            // 
            this.btnDelete.Location = new System.Drawing.Point(590, 407);
            this.btnDelete.Name = "btnDelete";
            this.btnDelete.Size = new System.Drawing.Size(98, 23);
            this.btnDelete.TabIndex = 6;
            this.btnDelete.Text = "Delete Line";
            this.btnDelete.UseVisualStyleBackColor = true;
            this.btnDelete.Visible = false;
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);
            // 
            // frmSeniorProjectHub
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1278, 435);
            this.Controls.Add(this.btnDelete);
            this.Controls.Add(this.lblStatus);
            this.Controls.Add(this.btnStart);
            this.Controls.Add(this.psbStatus);
            this.Controls.Add(this.txtResult);
            this.Controls.Add(this.picMain);
            this.Controls.Add(this.btnRight);
            this.Controls.Add(this.btnSelectImage);
            this.Controls.Add(this.btnLeft);
            this.Name = "frmSeniorProjectHub";
            this.Text = "Character Determiner";
            this.Load += new System.EventHandler(this.frmSeniorProjectHub_Load);
            ((System.ComponentModel.ISupportInitialize)(this.picMain)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnLeft;
        private System.Windows.Forms.Button btnRight;
        private System.Windows.Forms.Button btnSelectImage;
        private System.Windows.Forms.PictureBox picMain;
        private System.Windows.Forms.TextBox txtResult;
        private System.Windows.Forms.ProgressBar psbStatus;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.Button btnStart;
        private System.Windows.Forms.Label lblStatus;
        private System.Windows.Forms.Timer tmrProgressTracker;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
    }
}

