#
# Conditional build:
%bcond_without	vdpau		# build libav without VDPAU support
%bcond_with	system_libav	# system libav (note: upstream does not accept bugs with system libav)
%bcond_with	system_ffmpeg	# system ffmpeg instead of libav (unadvised, only some ffmpeg versions are compatible)

%define		gstname gst-libav
%define		gst_major_ver   1.0
%define		gst_req_ver	1.4.0
%define		gstpb_req_ver	1.4.0
%define		libav_ver	10.5
%define		ffmpeg_ver	2.2

%if %{with system_ffmpeg}
%define		with_system_libav	1
%endif
%include	/usr/lib/rpm/macros.gstreamer
Summary:	GStreamer Streaming-media framework plug-in using libav
Summary(pl.UTF-8):	Wtyczka do środowiska obróbki strumieni GStreamer używająca libav
Name:		gstreamer-libav
Version:	1.4.3
Release:	1
License:	LGPL v2+ (gst part), GPL v2+ (some libav parts)
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gst-libav/%{gstname}-%{version}.tar.xz
# Source0-md5:	248b6aae752710bbae77af01f74a082d
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	bzip2-devel
BuildRequires:	gstreamer-devel >= %{gst_req_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_req_ver}
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libtool
BuildRequires:	orc-devel >= 0.4.16
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.1
BuildRequires:	rpmbuild(macros) >= 1.470
%if %{with system_libav}
# libavformat,libavcodec,libavutil,libswscale needed
%if %{with system_ffmpeg}
BuildRequires:	ffmpeg-devel >= %{ffmpeg_ver}
%else
BuildRequires:	libav-devel >= %{libav_ver}
%endif
%else
# libav dependencies
BuildRequires:	SDL-devel
BuildRequires:	zlib-devel
%ifarch %{ix86} %{x8664}
BuildRequires:	yasm
%endif
%if %{with vdpau}
BuildRequires:	libvdpau-devel
BuildRequires:	xorg-lib-libXvMC-devel
%endif
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	gstreamer >= %{gst_req_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_req_ver}
%if %{with system_libav}
%if %{with system_ffmpeg}
BuildRequires:	ffmpeg-libs >= %{ffmpeg_ver}
%else
BuildRequires:	libav >= %{libav_ver}
%endif
%endif
Requires:	orc >= 0.4.16
Obsoletes:	gstreamer-ffmpeg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description apidocs
API documentation for GStreamer libav plugin.

%description apidocs -l pl.UTF-8
Dokumentacja API do wtyczki GStreamera libav.

%prep
%setup -q -n %{gstname}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	CPPFLAGS="%{rpmcppflags}" \
	%{?with_system_libav:--with-system-libav} \
	%{?with_vdpau:--with-libav-extra-configure="--enable-vdpau"} \
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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_major_ver}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/gstreamer-%{gst_major_ver}/libgstlibav.so
# disabled in (upstream) 1.2.0 until someone fixes it
#%attr(755,root,root) %{_libdir}/gstreamer-%{gst_major_ver}/libgstavscale.so

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gst-libav-plugins-1.0
