import os.path
from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain


class BoostConan(ConanFile):
    name = "boost"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "CMakeDeps"

    def configure(self):
        if self.settings.os == "Emscripten":
            self.options.shared = False

    def source(self):
        url = self.conan_data["sources"]["url"].format(version=self.version)
        conan.tools.files.get(self, url,
                            **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        exclude = ["nowide", "test"]
        if self.settings.os == "Emscripten":
            exclude += ["context", "coroutine", "asio", "fiber", "log"]
        tc.variables["BOOST_EXCLUDE_LIBRARIES"] = ";".join(exclude)
        tc.variables["BOOST_INSTALL_LAYOUT"] = "system"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs.append("lib/cmake")
        self.cpp_info.set_property("cmake_file_name", "boost_system")
