from pyPdf.pdf import PdfFileReader, PdfFileWriter, PageObject, RectangleObject, NameObject

import sys

def processFile(pdfFileNameIn, pdfFileNameOut) :
	pdfFile = readTheFile(pdfFileNameIn)
	columns = verticalColumns(pdfFile, 2)
	writer = PdfFileWriter()
	outputStream = file(pdfFileNameOut, "wb")
	splitWithColumns(pdfFile.pages, columns, writer, outputStream)
	outputStream.close()
	
def readTheFile(fName):
	 return PdfFileReader(file(fName, "rb"))
	
def verticalColumns(pdfFile, columnCount) :
	trimbox = pdfFile.getPage(0).trimBox
	initWidth = trimbox.lowerRight[0]
	fractionalWidth = initWidth / columnCount
	fragments = []
	for i in range(0, columnCount) : 
		frag = [fractionalWidth * i, fractionalWidth * (i + 1)]
		fragments.append(frag)
	return fragments
	
def splitWithColumns(pgs, columns, writer, outStream):
	for pg in pgs :
		split(pg, columns, writer, outStream)
	
def copyPage(page):
	newpage = PageObject(page.pdf)
	newpage.update(page)
	newpage[NameObject("/CropBox")] = RectangleObject(page.cropBox)
	return newpage	
	
def split(pg, columns, writer, stream):
	for i in range(0, len(columns)) :
		newPage = copyPage(pg)
		col = columns[i]
		newPage.cropBox.lowerLeft = [col[0], 0]
		newPage.cropBox.lowerRight = [col[1], 0]
		writer.addPage(newPage)
		writer.write(stream)

if __name__ == '__main__':
	processFile(sys.argv[1], sys.argv[2])