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
        filenames.push_back(ent->d_name);
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

  for (const auto& dirname : ListDirectory(video_dir)) {
    Student student(dirname);
    std::cout << "[*] Processing: " << student.id << " " << student.name << std::endl;

    for (const auto& filename : ListDirectory(video_dir + '/' + dirname)) {
      std::string old_filename = video_dir + '/' + dirname + '/' + filename;
      std::string new_filename = old_filename + "tmp";
      rename(old_filename.c_str(), new_filename.c_str());
    }

    int i = 0;
    for (const auto& filename : ListDirectory(video_dir + '/' + dirname)) {
      std::string old_filename = video_dir + '/' + dirname + '/' + filename;
      std::string new_filename = video_dir + '/' + dirname + '/' + student.name + '_' + std::to_string(i) + ".png";
      rename(old_filename.c_str(), new_filename.c_str());
      i++;
    }
  }
}
