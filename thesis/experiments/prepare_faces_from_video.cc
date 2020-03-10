#include <iostream>
#include <cstring>
#include <string>
#include <vector>

extern "C" {
#include <dirent.h>
#include <sys/stat.h>
}


struct Student final {
  Student(const std::string& filename)  // without ".mp4"
    : id(filename.substr(0, filename.find('_'))),
      name(filename.substr(filename.find('_') + 1)) {}
  const std::string id;
  const std::string name;
};


std::vector<std::string> ListDirectory(const std::string& directory) {
  DIR* dir = nullptr;
  dirent* ent = nullptr;
  std::vector<std::string> filenames;
  
  if ((dir = opendir(directory.c_str()))) {
    while ((ent = readdir(dir))) {
      if (strcmp(ent->d_name, ".") && strcmp(ent->d_name, "..")) {
        if (ent->d_type == DT_DIR) {
          std::cerr << "[WARNING] ignoring nested directory" << std::endl;
        } else {
          filenames.push_back(ent->d_name);
        }
      }
    }
    closedir(dir);
  }
  return filenames;
}


int main(int argc, char* args[]) {
  if (argc < 2) {
    std::cout << "usage: " << args[0] << " <directory>" << std::endl
              << "Videos in the given directory must be in this format: "
              << "U10516045_Wang_Guan_Zhong.mp4" << std::endl;
    return EXIT_SUCCESS;
  }

  const std::string video_dir(args[1]);

  for (const auto& filename : ListDirectory(video_dir)) {
    Student student(filename.substr(0, filename.rfind(".mp4")));
    std::cout << "[*] Processing: " << student.id << " " << student.name << std::endl;

    // Create student's directory.
    const std::string student_dir = student.id + "_" + student.name;
    mkdir((video_dir + '/' + student_dir).c_str(), 0755);

    // Extract frames using ffmpeg.
    const std::string vid_input = video_dir + '/' + filename;
    const std::string vid_output = video_dir + '/' + student_dir;
    const std::string cmd = std::string("ffmpeg -i '") + vid_input + "' -r 2 -start_number 0 '" + vid_output + "/" + student.name + "_\%d.png'";
    std::cout << cmd << std::endl;
    system(cmd.c_str());
  }
}
