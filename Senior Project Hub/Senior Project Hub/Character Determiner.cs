//Zachary Reese ~ Last Edit: 4/8/2021 ~ Hub for Senior Project. User inputs png image, which is then given to OCR Scanner for evaluation (with live updates on progress). After OCR Scanner gives results, the user is allowed to edit the results including editing text and deleting lines. The user also has the option to restart or save the results to a text file.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Senior_Project_Hub
{
    public partial class frmSeniorProjectHub : Form
    {
        string currentDirectory = Directory.GetCurrentDirectory();
        Image mainImage = null;
        int indexAccumulator = 0;
        public frmSeniorProjectHub()
        {
            InitializeComponent();
        }
        int intIndex = 0;
        List<Image> lstBoundingBoxes = new List<Image> {}; //Variable initialization
        List<string> lstResults = new List<string> {};
        private void btnSelectImage_Click(object sender, EventArgs e)
        {
            if (btnSelectImage.Text == "Select Image (PNG)") //Allows user to select image
            { //Start if
                openFileDialog1.InitialDirectory = currentDirectory;
                openFileDialog1.Filter = "Image Files(*.png)|*.png"; //Setting openfiledialog properties
                openFileDialog1.Title = "Select Paragraph Image (png)";
                if (openFileDialog1.ShowDialog() == DialogResult.OK) //user hasn't hit cancel
                { //start nested if
                    mainImage = Image.FromFile(openFileDialog1.FileName);
                    mainImage.Save(currentDirectory + "\\Data\\Original.png");
                    picMain.Image = mainImage;
                    picMain.Visible = true;
                    btnStart.Visible = true;
                } //end nested if
            } else{
                //saves results to text file
                saveFileDialog1.InitialDirectory = currentDirectory;
                saveFileDialog1.Filter = "txt files (*.txt)|*.txt|All files (*.*)|*.*";
                saveFileDialog1.Title = "Select Location to Store Text File";
                if (saveFileDialog1.ShowDialog() == DialogResult.OK)
                { //start nested if
                    File.WriteAllLines(saveFileDialog1.FileName, lstResults);
                    restartProperties();
                } //end nested if

            } //end if
        } //end class

        private void restartProperties() //Changes form object properties when the program restarts process
        {
            txtResult.Visible = false;
            btnLeft.Visible = false;
            btnRight.Visible = false;
            btnDelete.Visible = false;
            btnStart.Text = "Start";
            btnSelectImage.Text = "Select Image (PNG)";
            picMain.Image.Dispose();
            picMain.Visible = false;
            btnStart.Visible = false;
            txtResult.Clear();
            lstBoundingBoxes.Clear();
            lstResults.Clear();
            intIndex = 0;
        } //end void

        private void startProcess()
        {
            btnSelectImage.Visible = false;
            btnSelectImage.Text = "Save to Text File";
            btnStart.Visible = false;
            btnStart.Text = "Restart";
            psbStatus.Visible = true;
            lblStatus.Visible = true;
            using (StreamWriter writer = new StreamWriter(currentDirectory + "\\Data\\Status.txt"))
            {
                writer.WriteLine("Initializing Process");
                writer.WriteLine(Convert.ToString(indexAccumulator));
            }

            Process proc = new Process();
            proc.StartInfo.UseShellExecute = false;
            proc.StartInfo.FileName = "C:\\Users\\zcrzc\\AppData\\Local\\Programs\\Python\\Python38\\python.exe"; //BCTC
                                                                                                                  //proc.StartInfo.FileName = "C:\\Users\\zcrzc\\AppData\\Local\\Programs\\Python\\Python38\\python.exe"; //HOME
                                                                                                                  //proc.StartInfo.FileName = "C:\\Users\zcrzc\\AppData\Local\\Programs\\Python\\Python38\\python.exe"; //LAPTOP
                                                                                                                  //proc.StartInfo.FileName = "C:\\Users\\z_reese\\AppData\\Local\\Programs\\Python\\Python38\\python.exe"; //BCTC
            proc.StartInfo.Arguments = "\"" + currentDirectory + "\\Data\\OCR Scanner.py\"";
            proc.StartInfo.CreateNoWindow = true;
            proc.Start();
            tmrProgressTracker.Enabled = true;
            txtResult.Visible = false;
        }

        private void btnStart_Click(object sender, EventArgs e)
        { //Starts OCR Scanner
            if (btnStart.Text == "Start"){

                startProcess();

            } else{ //restarts program process for another instance
                if (MessageBox.Show("Are you sure you want to restart the process?", "Delete Line?", MessageBoxButtons.YesNo) == DialogResult.Yes)
                    restartProperties();
            } //end if
        } //end void
        private void tmrProgressTracker_Tick(object sender, EventArgs e)
        {
            try //checks for the status of OCR Scanner
            {
                var lines = File.ReadAllLines(currentDirectory + "\\Data\\Status.txt");
                if (lines[1] != "-1") {
                    lblStatus.Text = Convert.ToString(lines[0]); //updates scan status on form
                    psbStatus.Value = Convert.ToInt32(lines[1]);
                    if (lines[1] == "100") //OCR Scanner has completed its scan
                    {
                        tmrProgressTracker.Enabled = false;
                        var line = File.ReadAllLines(currentDirectory + "\\Data\\Results.txt");
                        foreach (var result in line)
                        {
                            lstResults.Add(Convert.ToString(result));
                        } //end foreach
                        int tempacc = 0;
                        for (int acc = 0; acc < lstResults.Count; acc += 1)
                        {
                            lstBoundingBoxes.Add(Image.FromFile(currentDirectory + "\\Data\\BoundingBoxes\\BoundingBoxImage" + Convert.ToString(acc + indexAccumulator) + ".png"));
                            tempacc += 1;
                        } //end for
                        indexAccumulator += tempacc;
                        picMain.Image = lstBoundingBoxes[0];
                        txtResult.Text = lstResults[0];
                        txtResult.Visible = true;
                        btnSelectImage.Visible = true;
                        lblStatus.Visible = false;
                        btnLeft.Visible = true;
                        btnRight.Visible = true;
                        btnDelete.Visible = true;
                        btnStart.Visible = true;
                        psbStatus.Visible = false;
                        psbStatus.Value = 0;
                    } //end nested if
                } else {
                    psbStatus.Value = 0;
                    lstBoundingBoxes.Clear();
                    lstResults.Clear();
                    startProcess();
                } //end if
            } catch (Exception ex) { } //end try
        } //end void

        private void btnLeft_Click(object sender, EventArgs e) //Moves slide image one left
        {
            intIndex -= 1;
            if (intIndex == -1)
                intIndex = lstResults.Count - 1;
            picMain.Image = lstBoundingBoxes[intIndex];
            txtResult.Text = lstResults[intIndex];
        } //end void

        private void btnRight_Click(object sender, EventArgs e) //Moves slide image on right
        {
            intIndex += 1;
            if (intIndex == lstResults.Count)
                intIndex = 0;
            picMain.Image = lstBoundingBoxes[intIndex];
            txtResult.Text = lstResults[intIndex];
        } //end void

        private void txtResult_TextChanged(object sender, EventArgs e) //Autosaves text changes
        {
            lstResults[intIndex] = txtResult.Text;
        } //end void

        private void btnDelete_Click(object sender, EventArgs e) //Deletes a line and its related content
        {
            if (MessageBox.Show("Are you sure you want to delete line #" + Convert.ToString(intIndex + 1) + "?", "Delete Line?", MessageBoxButtons.YesNo) == DialogResult.Yes)
            { //start if
                if (lstResults.Count - 1 == 0) //start nested if
                {
                    txtResult.Text = "There are no lines remaining... automatically restarting the process.";
                    restartProperties();
                } else {
                    lstBoundingBoxes.RemoveAt(intIndex);
                    lstResults.RemoveAt(intIndex);
                    intIndex -= 1;
                    if (intIndex == -1)
                        intIndex = 0;
                    picMain.Image = lstBoundingBoxes[intIndex];
                    txtResult.Text = lstResults[intIndex];
                } //end nested if
            } //end if
        } //end void

        private void frmSeniorProjectHub_Load(object sender, EventArgs e)
        {
            string[] filePaths = Directory.GetFiles(currentDirectory + "\\Data\\BoundingBoxes\\");
            foreach (string filePath in filePaths)
            {
                File.SetAttributes(filePath, FileAttributes.Normal);
                File.Delete(filePath);
            } //end foreach
        } //end void
    } //end class
} //end namespace