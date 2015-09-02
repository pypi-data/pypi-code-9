def _zip_external(base_dir, archive_path):
  popenargs = shell_expand_to_popen("zip -q -r $ARCHIVE $DIR", {"ARCHIVE": archive_path, "DIR": "."})
  cd_to = base_dir
  log.debug("using cwd: %s", cd_to)
  log.info("compress: %s", " ".join(popenargs))
  subprocess.check_call(popenargs, cwd=cd_to, stdout=SHELL_OUTPUT, stderr=SHELL_OUTPUT, stdin=DEV_NULL)


def _zip_python(base_dir, archive_path):
  zip = zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True)
  try:
    for dirpath, dirnames, filenames in os.walk(base_dir):
      for name in filenames:
        path = os.path.normpath(os.path.join(dirpath, name))
        log.info("Adding %s", path)
        zip.write(path, path)
  finally:
    zip.close()