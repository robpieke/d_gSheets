#include <Python.h>
#include <ndspy.h>
#include <sstream>

PtDspyError DspyImageOpen(
		PtDspyImageHandle *image,
		const char *drivername,
		const char *filename,
		int width,
		int height,
		int paramCount,
		const UserParameter *parameters,
		int formatCount,
		PtDspyDevFormat *format,
		PtFlagStuff *flagstuff)
{
	// Initialise the python interpreter
	// (ensure cwd ends up part of sys.path)
	//
	Py_SetProgramName("d_gSheets");
	Py_Initialize();
	char *argv0 = nullptr;
	PySys_SetArgv(0, &argv0);

	char cmd[1024];
	sprintf(cmd,
			"import py_gSheets\n"
			"gBuffer = py_gSheets.GBuffer(%d, %d, ['%s',])\n",
			width, height, "rgba"
	);
	PyRun_SimpleString(cmd);

	return PkDspyErrorNone;
}

PtDspyError DspyImageData(
		PtDspyImageHandle image,
		int xmin,
		int xmax_plus_one,
		int ymin,
		int ymax_plus_one,
		int entrysize,
		const unsigned char *data)
{
	std::stringstream ss;
	ss << "gBuffer.updateCells("
	   << ymin << "," << ymax_plus_one << ","
	   << xmin << "," << xmax_plus_one << ","
	   << "[";
	const float *fData = reinterpret_cast<const float*>(data);
	for(int i = 0; i < (xmax_plus_one-xmin) * (ymax_plus_one-ymin); ++i)
	{
		ss << "(" << fData[i*4+1] << "," << fData[i*4+2] << "," <<fData[i*4+3] << "),";
	}
	ss << "])\n";
	PyRun_SimpleString(ss.str().c_str());
	return PkDspyErrorNone;
}

PtDspyError DspyImageClose(
		PtDspyImageHandle pvImage)
{
	Py_Finalize();
	return PkDspyErrorNone;
}

PtDspyError DspyImageQuery(
		PtDspyImageHandle pvImage,
		PtDspyQueryType type,
		int size,
		void *p)
{
	switch(type)
	{
		case PkSizeQuery:
		case PkOverwriteQuery:
		case PkNextDataQuery:
		case PkRedrawQuery:
		case PkRenderingStartQuery:
		case PkSupportsCheckpointing:
		case PkPointCloudQuery:
		case PkGridQuery:
		case PkMultiResolutionQuery:
		case PkQuantizationQuery:
		case PkMemoryUsageQuery:
		case PkElapsedTimeQuery:
			return PkDspyErrorUnsupported;
		default:
			return PkDspyErrorUndefined;
	}
}
