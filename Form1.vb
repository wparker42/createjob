Imports System.IO





Public Class Form1

    Public selecteddrive


    Private Sub Button2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button2.Click
        End

    End Sub

    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click

        Dim parline, parline1, parline2, parsefilename As String

        Dim ret


        selecteddrive = drivesbox.SelectedItem

        If civil.Checked Then
            parsefilename = "createjob_civ.txt"
        ElseIf environmental.Checked Then
            parsefilename = "createjob_env.txt"
        ElseIf structural.Checked Then
            parsefilename = "createjob_stc.txt"
        Else
            MsgBox("No Selection")
            Exit Sub
        End If

        If TextBox1.Text <> "" Then
            If My.Computer.FileSystem.DirectoryExists(selecteddrive & TextBox1.Text) Then
                MsgBox("Folder exists")
            Else
                My.Computer.FileSystem.CreateDirectory(selecteddrive & TextBox1.Text)
                My.Computer.FileSystem.CreateDirectory(selecteddrive & TextBox1.Text & "\_" & TextBox2.Text)

                FileOpen(1, parsefilename, OpenMode.Input)
                While Not EOF(1)
                    parline = LineInput(1)
                    If parline.StartsWith("!") Then
                        parline = parline.Substring(1)
                        parline = Replace(parline, "#", TextBox1.Text & " - ")
                        ret = parline.IndexOf("|")
                        parline1 = parline.Substring(0, ret)

                        parline2 = parline.Substring(ret + 1)
                        FileCopy(parline1, selecteddrive & TextBox1.Text & "\" & parline2)


                    ElseIf parline.StartsWith(";") Then

                    Else


                        My.Computer.FileSystem.CreateDirectory(selecteddrive & TextBox1.Text & "\" & parline)

                    End If

                End While
                FileClose(1)
                'FileCopy("C:\createjob.txt",
            End If
        End If




        ret = MsgBox("Job folder created", MsgBoxStyle.OkOnly)
        If ret = 1 Then End



    End Sub

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        For Each drive As System.IO.DriveInfo In System.IO.DriveInfo.GetDrives()
            If drive.IsReady Then

                drivesbox.Items.Add(drive.Name)
            End If
        Next
        drivesbox.SelectedIndex = 0


    End Sub




End Class
