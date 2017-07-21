#include "itkImage.h"
#include "itkImageFileReader.h"
#include "itkSignedMaurerDistanceMapImageFilter.h"
#include "itkImageFileWriter.h"
#include <sstream>
#include "SignedMaurerDistanceMapImageFilterCLP.h"

typedef itk::Image<unsigned char, 3>  UnsignedCharImageType;
typedef itk::Image<float, 3>          FloatImageType;

int main(int argc, char * argv[])
{

    PARSE_ARGS;
    UnsignedCharImageType::Pointer image = UnsignedCharImageType::New();

    typedef itk::ImageFileReader<UnsignedCharImageType> ReaderType;
    ReaderType::Pointer reader = ReaderType::New();
    reader->SetFileName(inputfile);
    reader->Update();
    image = reader->GetOutput();

    typedef  itk::SignedMaurerDistanceMapImageFilter< UnsignedCharImageType, FloatImageType  > SignedMaurerDistanceMapImageFilterType;
    SignedMaurerDistanceMapImageFilterType::Pointer distanceMapImageFilter =
            SignedMaurerDistanceMapImageFilterType::New();
    distanceMapImageFilter->SetInput(image);

    typedef itk::ImageFileWriter< FloatImageType >  WriterType;
    WriterType::Pointer writer = WriterType::New();
    writer->SetFileName(outputfile);
    writer->SetInput(distanceMapImageFilter->GetOutput());
    writer->Update();


    return EXIT_SUCCESS;
}
