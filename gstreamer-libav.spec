#
# Conditional build:
%bcond_without	gpl		# GPL licensed components
%bcond_without	vdpau		# build libav without VDPAU support
%bcond_with	system_ffmpeg	# system ffmpeg (note: upstream does not accept bugs with system ffmpeg)

%define		gstname		gst-libav
%define		gstmver		1.0
%define		gst_ver		1.16.3
%define		gstpb_ver	1.16.3
%define		ffmpeg_ver	4.1.3

Summary:	GStreamer Streaming-media framework plug-in using libav
Summary(pl.UTF-8):	Wtyczka do środowiska obróbki strumieni GStreamer używająca libav
Name:		gstreamer-libav
Version:	1.16.3
Release:	1
%if %{with gpl}
License:	GPL v2+
%else
License:	LGPL v2+
%endif
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gst-libav/%{gstname}-%{version}.tar.xz
# Source0-md5:	d08fb5429f102d5a3f1eca3dee2a0add
Patch0:		link.patch
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	orc-devel >= 0.4.16
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 2.1
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.470
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with system_ffmpeg}
# libavformat,libavcodec >= 57,libavutil,libswscale needed
BuildRequires:	ffmpeg-devel >= %{ffmpeg_ver}
%else
# libav dependencies
BuildRequires:	bzip2-devel
BuildRequires:	libvdpau-devel
BuildRequires:	xorg-lib-libX11-devel
%if %{with vdpau}
BuildRequires:	xorg-lib-libXvMC-devel
%endif
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%ifarch %{ix86} %{x8664}
BuildRequires:	yasm
%endif
%endif
Requires:	glib2 >= 1:2.40.0
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
%if %{with system_ffmpeg}
Requires:	ffmpeg-libs >= %{ffmpeg_ver}
%endif
Requires:	orc >= 0.4.16
Obsoletes:	gstreamer-ffmpeg
Obsoletes:	gstreamer-real
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
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for GStreamer libav plugin.

%description apidocs -l pl.UTF-8
Dokumentacja API do wtyczki GStreamera libav.

%prep
%setup -q -n %{gstname}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}

LIBAV_OPTS="%{?with_vdpau:--enable-vdpau}"
%ifarch x32
LIBAV_OPTS="$LIBAV_OPTS --disable-asm"
%endif
%configure \
	CPPFLAGS="%{rpmcppflags}" \
	%{?with_system_ffmpeg:--with-system-libav} \
	--with-libav-extra-configure="$LIBAV_OPTS" \
	%{?with_gpl:--enable-gpl} \
	--disable-silent-rules \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}

# V=1 is for libav (--disable-silent-rules affects only main gst-libav sources)
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gstmver}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/gstreamer-%{gstmver}/libgstlibav.so
# disabled in (upstream) 1.2.0 until someone fixes it
#%attr(755,root,root) %{_libdir}/gstreamer-%{gstmver}/libgstavscale.so

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gst-libav-plugins-1.0
