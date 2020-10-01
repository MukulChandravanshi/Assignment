# Import libraries


def Media_Cop_ScannedPdf(Pdf_path,OutputFolder_Path,Popper_Path,OCR_path):

        from PIL import Image
        import pytesseract
        import sys
        from pdf2image import convert_from_path
        import os
        import PyPDF2
        from datetime import date
        import tabula
        from PyPDF2 import PdfFileWriter, PdfFileReader
        from tabula import read_pdf



        #PDF_file = "RESMY-SG-TMEEN001-2118001260 stb.pdf"

        #List for storing the text & InvoiceNumber
        Pdf_text = []
        Invoice_NumberList = []

        # Store all the pages of the PDF in a variable
        pages = convert_from_path(Pdf_path,500,poppler_path = Popper_Path)

        # Counter to store images of each page of PDF to image
        image_counter = 1

        # Iterate through all the pages stored above
        for page in pages:
            filename = "page_" + str(image_counter) + ".jpg"

            # Save the image of the page in system
            page.save(filename, 'JPEG')

        # Increment the counter to update filename
        image_counter = image_counter + 1

        # Variable to get count of total number of pages
        filelimit = image_counter - 1


        # Iterate from 1 to total number of pages
        for i in range(1, filelimit + 1):
            filename = "page_" + str(i) + ".jpg"

            # Recognize the text as string in image using pytesserct
            pytesseract.pytesseract.tesseract_cmd = OCR_path
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace('\n', '')

            Pdf_text.clear()
            Invoice_NumberList.clear()
            Pdf_text = list(text.split(" "))

            #Loop for all items of list

        for i in range(0, len(Pdf_text)-1):
            List_value = Pdf_text[i]

            #Checking the totalist items
            if i < len(Pdf_text):
                List_value_next = Pdf_text[i+1]

            if List_value.__contains__("Invoice") and List_value_next.__contains__("No."):
                Invoice_Number = Pdf_text[i+3]
                Invoice_Number = str(Invoice_Number).replace("Date","")
                Invoice_NumberList.append(Invoice_Number)
                print(str(Invoice_Number))

        Invoice_NumberList.append("NULL")
        totalPdfCount = []
        PagesInPdf = 1
        distinctPdfInvoices = []

        for i in range(0, len(Invoice_NumberList) - 1):
            if Invoice_NumberList[i] != Invoice_NumberList[i + 1]:
                totalPdfCount.append(PagesInPdf)
                distinctPdfInvoices.append(Invoice_NumberList[i])
                PagesInPdf = 1
            else:
                PagesInPdf += 1

        read_pdf2 = PyPDF2.PdfFileReader(Pdf_path)
        countPdf = 0
        pageNumber = 0
        for i in range(0, len(totalPdfCount)):
            output = PdfFileWriter()
            for j in range(0, totalPdfCount[i]):
                output.addPage(read_pdf2.getPage(pageNumber))
                pageNumber += 1
            countPdf += 1

            pdfFileName = path_leaf(Pdf_path).lower().replace(".pdf", "").replace(".PDF", "")

            IsDistinctPdfFolderExists = os.path.isdir(OutputFolder_Path)

            if IsDistinctPdfFolderExists == True:
                print(OutputFolder_Path)
            else:
                os.mkdir(OutputFolder_Path)

            outPutPdf = f'{OutputFolder_Path}\\IBS_{pdfFileName}_{distinctPdfInvoices[i].replace("/", "_").strip()}.pdf'
            with open(outPutPdf, "wb") as outputStream:
                output.write(outputStream)

def read_Pdf(filePath, outPutPath):
    import PyPDF2
    import re
    import os
    from datetime import date
    import tabula
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from tabula import read_pdf
    import  fitz


    ReadPDF = PyPDF2.PdfFileReader(filePath)

    #Addedby Mukul--Today's date folder
    #today = (date.today()).strftime('%d-%b-%Y')
    #outPutPath_TodayDate: Union[bytes, str] = os.path.join(outPutPath,today)
    IsDateFolderExists = os.path.isdir(outPutPath)

    if IsDateFolderExists == True:
        print(outPutPath)
    else:
        os.mkdir(outPutPath)

    PdfEstimateNumberList=[]
    Pages = ReadPDF.getNumPages()

    for page in range(1,ReadPDF.getNumPages()+1):
        df=read_pdf(filePath,area = (10,10,1000,1000),
                    stream=True
                    ,pandas_options={'header': None}
                    ,pages = page,
                    guess=False)


        for rowIndex, row in df.iterrows():
            for colIndex in range(1, df.shape[1]):
                row[0] = str(row[0]) + "|" + str(row[colIndex]);
            if(str(row[0]).__contains__("Invoice Number :")):
                Invoice_RowNo = rowIndex
                print(row[0])
                estimateNum = str(row[0]).split("Number : ")[1][:10]
                PdfEstimateNumberList.append(estimateNum);
                # estimateNum=str(row[0]).replace("Invoice Number.","").replace("nan","").strip();
            elif (str(row[0]).__contains__("Credit Note Number :")):
                Invoice_RowNo = rowIndex
                print(row[0])
                estimateNum = str(row[0]).split("Number : ")[1][:10]
                PdfEstimateNumberList.append(estimateNum);
            elif (str(row[0]).__contains__("Debit Note Number :")):
                Invoice_RowNo = rowIndex
                print(row[0])
                estimateNum = str(row[0]).split("Number : ")[1][:10]
                PdfEstimateNumberList.append(estimateNum);

    PdfEstimateNumberList.append("NULL")
    totalPdfCount = []
    PagesInPdf = 1
    distinctPdfInvoices=[]

    for i in range(0, len(PdfEstimateNumberList) - 1):
        if PdfEstimateNumberList[i] != PdfEstimateNumberList[i + 1]:
            totalPdfCount.append(PagesInPdf)

            #Added By Bharat to Store distinct Invoice Number
            distinctPdfInvoices.append(PdfEstimateNumberList[i])
            PagesInPdf = 1
        else:
            PagesInPdf += 1

    read_pdf2 = PyPDF2.PdfFileReader(filePath)
    countPdf = 0
    pageNumber = 0
    for i in range(0, len(totalPdfCount)):
        output = PdfFileWriter()
        for j in range(0, totalPdfCount[i]):
            output.addPage(read_pdf2.getPage(pageNumber))
            pageNumber += 1
        countPdf += 1

        pdfFileName = path_leaf(filePath).lower().replace(".pdf", "").replace(".PDF","")

        #added by Mukul---Create folder PE wise
        #outPutPath = os.path.join(outPutPath_TodayDate,distinctPdfInvoices[i].replace("/","_").strip())
        IsDistinctPdfFolderExists = os.path.isdir(outPutPath)

        if IsDistinctPdfFolderExists==True:
            print(outPutPath)
        else:
            os.mkdir(outPutPath)

        outPutPdf =  f'{outPutPath}\\IBS_{pdfFileName}_{distinctPdfInvoices[i].replace("/","_").strip()}.pdf'
        with open(outPutPdf, "wb") as outputStream:
            output.write(outputStream)

def read_Pdf_PM_Precision(filePath, outPutPath):
    import PyPDF2
    import re
    import os
    from datetime import date
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from tabula import read_pdf

    ReadPDF = PyPDF2.PdfFileReader(filePath)
    PdfEstimateNumberList=[]

    for page in range(1,ReadPDF.getNumPages()+1):
        df=read_pdf(filePath,area = (231.678,265.890,298.615,546.283),
                    stream=True
                    ,pandas_options={'header': None}
                    ,pages = page,
                    guess=False)
        estimateNum = ""

        #Extracting Invoice Number
        estimateNum=str(df.loc[0][1]).strip()
        PdfEstimateNumberList.append(estimateNum);



    PdfEstimateNumberList.append("NULL")
    totalPdfCount = []
    PagesInPdf = 1
    distinctPdfInvoices=[]

    #MATCH the invoice numbers
    for i in range(0, len(PdfEstimateNumberList) - 1):
        if PdfEstimateNumberList[i] != PdfEstimateNumberList[i + 1]:
            totalPdfCount.append(PagesInPdf)
            distinctPdfInvoices.append(PdfEstimateNumberList[i])
            PagesInPdf = 1
        else:
            PagesInPdf += 1


    read_pdf2 = PyPDF2.PdfFileReader(filePath)
    countPdf = 0
    pageNumber = 0
    for i in range(0, len(totalPdfCount)):
        output = PdfFileWriter()
        for j in range(0, totalPdfCount[i]):
            # totalPdfCount[i]
            output.addPage(read_pdf2.getPage(pageNumber))
            pageNumber += 1
        countPdf += 1


        pdfFileName = path_leaf(filePath).lower().replace(".pdf", "").replace(".PDF","")
        IsDistinctPdfFolderExists = os.path.isdir(outPutPath)

        if IsDistinctPdfFolderExists == True:
            print(outPutPath)
        else:
            os.mkdir(outPutPath)

        outPutPdf = f'{outPutPath}\\{pdfFileName}_{distinctPdfInvoices[i].replace("/", "_").strip()}.pdf'

        with open(outPutPdf, "wb") as outputStream:
            output.write(outputStream)


def path_leaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


if __name__ == "__main__":
    import sys
    import time
    import os
    import tabula
    from tabula import  read_pdf

    start_time = time.time()
    print('Process Start')
    try:
        #raise()
        Pdf_path = sys.argv[1]
        OutputFolder_Path = sys.argv[2]
        Popper_Path = sys.argv[3]
        OCR_path = sys.argv[4]
        Vendor_Name = sys.argv[5]

        print("Checking the pdf Format....")
        df = read_pdf(Pdf_path, area=(10, 10, 1000, 1000),
                      stream=True
                      , pandas_options={'header': None}
                      , pages=1,
                      guess=False)


        if Vendor_Name == "PM Precision":
            print("Executing read_Pdf_PM_Precision")
            read_Pdf_PM_Precision(Pdf_path, OutputFolder_Path)
        else:

            if df is not None:
                read_Pdf(Pdf_path, OutputFolder_Path)
            else:
                Media_Cop_ScannedPdf(Pdf_path, OutputFolder_Path, Popper_Path, OCR_path)
        print('Process End')
        print("Time taken to process your document : " + str(time.time() - start_time))
    except Exception as e:
        print("An exception occurred"+e.__str__())
        raise e
