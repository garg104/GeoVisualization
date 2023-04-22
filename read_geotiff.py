import numpy as np
import vtk 
from vtk.util import numpy_support 
import argparse
from tifffile import TiffFile, imread
import zarr  # type: ignore


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import GeoTIFF file into VTK dataset')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input filename')
    parser.add_argument('-o', '--output', type=str, help='Output filename for VTK dataset')
    parser.add_argument('--band', type=int, default=0, help='Band to select')
    args = parser.parse_args()

    tif = TiffFile(args.input)
    print(tif)

    if not tif.is_geotiff:
        raise Exception("Not a geotiff file")

    store = tif.aszarr(key=args.band)
    z = zarr.open(store, mode="r")
    store.close()
    zz = np.array(z)
    zz = np.flip(zz, axis=0)
    shape = z.shape
    print(f'metadata:\n{tif.geotiff_metadata}')
    xform = np.array(tif.geotiff_metadata['ModelTransformation'])
    img = vtk.vtkImageData()
    vals = numpy_support.numpy_to_vtk(zz.flatten())
    img.SetDimensions(shape[1], shape[0], 1)
    img.SetSpacing(xform[0,0], -xform[1,1], 1)
    img.SetOrigin(xform[0,3], -xform[1,3], 0)
    img.GetPointData().SetScalars(vals)

    if args.output is not None:
        writer = vtk.vtkXMLImageDataWriter()
        writer.SetInputData(img)
        writer.SetFileName(args.output)
        writer.Write()


    _min = np.min(zz)
    _max = np.max(zz)

    ctf = vtk.vtkColorTransferFunction()
    ctf.AddRGBPoint(-25, 0.8, 1, 1)
    ctf.AddRGBPoint(0, 0, 0, 1)
    ctf.AddRGBPoint(12.5, 1, 0, 0)
    ctf.AddRGBPoint(45, 1, 1, 0)
    ctf.AddRGBPoint(99999, 0, 0, 0)
    print(f'min={_min}, max={_max}')
    # mapper = vtk.vtkDataSetMapper()
    # mapper.ScalarVisibilityOn()
    # mapper.SetLookupTable(ctf)
    # mapper.SetInputData(img)
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)
    # renderer = vtk.vtkRenderer()
    # renderer.AddActor(actor)
    # window = vtk.vtkRenderWindow()
    # window.SetSize(1024, 1024)
    # window.AddRenderer(renderer)
    # interactor = vtk.vtkRenderWindowInteractor()
    # interactor.SetRenderWindow(window)
    # interactor.Initialize()
    # # window.Render()
    # interactor.Start()


    print(xform)
