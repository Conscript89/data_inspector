Name: data_inspector
Version: 0.0.1
Release: 1%{?dist}

Summary: Data inspector
License: BSD
BuildArch: noarch

URL: https://github.com/Conscript89/data_inspector
Source0: https://github.com/Conscript89/data_inspector/releases/download/%{version}/data_inspector-%{version}.tar.gz

%generate_buildrequires
%pyproject_buildrequires

%description
Data inspector

%prep
%autosetup


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files data_inspector

%files -f %{pyproject_files}
%{_bindir}/data_inspector

%changelog
* Sat Mar 16 2024 Pavel Holica <conscript89@gmail.com> - 0.0.1-1
- Initial specfile
