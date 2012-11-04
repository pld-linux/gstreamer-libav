#
# Conditional build:
%bcond_without	vdpau		# build libav without VDPAU support
%bcond_with	system_libav	# system libav (note: upstream does not accept bugs with system libav)

%define		gstname gst-libav
%define		gst_major_ver   1.0
%define		gst_req_ver	1.0.0

%include	/usr/lib/rpm/macros.gstreamer
Summary:	GStreamer Streaming-media framework plug-in using libav
Summary(pl.UTF-8):	Wtyczka do środowiska obróbki strumieni GStreamer używająca libav
Name:		gstreamer-libav
Version:	1.0.2
Release:	1
# the libav plugin is LGPL, the postproc plugin is GPL
License:	GPL v2+ and LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gst-libav/%{gstname}-%{version}.tar.xz
# Source0-md5:	b932d386711a1b14d08c3b7d3021934b
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
BuildRequires:	bzip2-devel
BuildRequires:	gstreamer-devel >= %{gst_req_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gst_req_ver}
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libtool
BuildRequires:	orc-devel >= 0.4.6
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.1
BuildRequires:	rpmbuild(macros) >= 1.470
%if %{with system_libav}
# libavformat,libavcodec,libavutil,libpostproc,libswscale needed
BuildRequires:	libav-devel
%else
# TODO: fill the rest of libav dependencies used here
%if %{with vdpau}
BuildRequires:	libvdpau-devel
BuildRequires:	xorg-lib-libXvMC-devel
%endif
%endif
Requires:	gstreamer-plugins-base >= %{gst_req_ver}
Requires:	orc >= 0.4.6
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
	--disable-static
%{__make}

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
%attr(755,root,root) %{_libdir}/gstreamer-%{gst_major_ver}/libgstavscale.so
