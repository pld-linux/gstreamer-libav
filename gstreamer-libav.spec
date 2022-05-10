#
# Conditional build:
%bcond_without	apidocs		# API documentation

%define		gstname		gst-libav
%define		gstmver		1.0
%define		gst_ver		1.20.0
%define		gstpb_ver	1.20.0
%define		ffmpeg_ver	4.4

Summary:	GStreamer Streaming-media framework plug-in using libav
Summary(pl.UTF-8):	Wtyczka do środowiska obróbki strumieni GStreamer używająca libav
Name:		gstreamer-libav
Version:	1.20.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gst-libav/%{gstname}-%{version}.tar.xz
# Source0-md5:	30ec3fe428b9e2a6ba9326d34bd37a4d
URL:		https://gstreamer.freedesktop.org/
# libavfilter >= 7.16.100, libavformat >= 58.12.100, libavcodec >= 58.18.100, libavutil >= 56.14.100
BuildRequires:	ffmpeg-devel >= %{ffmpeg_ver}
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
%{?with_apidocs:BuildRequires:	hotdoc >= 0.11.0}
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 2.1
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	ffmpeg-libs >= %{ffmpeg_ver}
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
Obsoletes:	gstreamer-ffmpeg < 1
Obsoletes:	gstreamer-real < 1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout	-flto

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plug-ins.

This plugin contains the libav codecs, containing codecs for most
popular multimedia formats.

%description -l pl.UTF-8
GStreamer to środowisko obróbki danych strumieniowych, bazujące na
grafie filtrów operujących na danych medialnych. Aplikacje używające
tej biblioteki mogą robić wszystko od przetwarzania dźwięku w czasie
rzeczywistym, do odtwarzania filmów i czegokolwiek innego związanego z
mediami. Architektura bazująca na wtyczkach pozwala na łatwe dodawanie
nowych typów danych lub możliwości obróbki.

Wtyczka ta zawiera kodeki libav, potrafiące zdekodować
najpopularniejsze formaty multimedialne.

%package apidocs
Summary:	API documentation for GStreamer libav plugin
Summary(pl.UTF-8):	Dokumentacja API do wtyczki GStreamera libav
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for GStreamer libav plugin.

%description apidocs -l pl.UTF-8
Dokumentacja API do wtyczki GStreamera libav.

%prep
%setup -q -n %{gstname}-%{version}

%build
%meson build \
	--default-library=shared \
	%{!?with_apidocs:-Ddoc=disabled}

%ninja_build -C build

%if %{with apidocs}
cd build/docs
LC_ALL=C.UTF-8 hotdoc run --conf-file libav-doc.json
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
cp -pr build/docs/libav-doc $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/gstreamer-%{gstmver}/libgstlibav.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gstreamer-%{gstmver}/libav-doc
%endif
