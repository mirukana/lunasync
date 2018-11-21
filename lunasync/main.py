# Copyright 2018 miruka
# This file is part of lunasync, licensed under LGPLv3.

from pathlib import Path
from typing import Dict, Optional, Sequence, Union

from lunafind import Stream

from . import LOG, config, savedata


def sync(subs:            Optional[Sequence[Dict[str, Optional[str]]]] = None,
         only_for_labels: Sequence[str]    = (),
         force_full:      bool             = False,
         base_dir:        Union[str, Path] = Path("."),
         overwrite:       bool             = False,
         warn:            bool             = False) -> int:
    """Start tag search synchronizations, return number of posts downloaded.

    Arguments:
      subs:
        sequence of dicts representing a search,
        See lunasync.config.FIELDS for the required dict keys.
        Values can be empty.
        If None, searches will be read from the user's config file.

      only_for_labels:
        If specified, only sync for searches with these labels.

      force_full:
        If True, force running full synchronizations, rechecking every posts.

      base_dir:
        Where to download posts. Defaults to current directory.

      overwrite:
        Whether to force downloads and overwrite existing files, or skip them.
        Defaults to False (skip).

      warn:
        If warnings must be shown when skipping existing files.
        Defaults to False."""

    subs_in_cfg = False
    downloaded  = 0

    for sub in subs or config.SUBS:
        subs_in_cfg = True

        sub = {k: "" if v is None or v.strip() == "%" else v.strip()
               for k, v in sub.items()}

        if only_for_labels and \
           not any(l in only_for_labels for l in sub["labels"].split()):
            continue

        savedata.reload()

        try:
            sub_data = savedata.DATA[str(sub)]
        except KeyError:
            savedata.DATA[str(sub)] = {"last_id": 0, "success": None}
            sub_data                = savedata.DATA[str(sub)]

        stream = Stream(sub["tag_search"],
                        pages  = "all",
                        limit  = 200,
                        client = sub["booru"] or None).filter(sub["filter"])

        if not force_full:
            stream = stream.stop_if("id:<=%s" % sub_data["last_id"])

        sub_data["success"] = False

        try:
            newest_id   = sub_data["last_id"]
            newest_post = next(stream)
            newest_id   = newest_post.id

            newest_post.download(
                base_dir=base_dir,overwrite=overwrite, warn=warn
            )
            stream.download(base_dir=base_dir, overwrite=overwrite, warn=warn)

        except StopIteration:
            pass

        except Exception:
            savedata.write()
            raise

        try:
            # Verify everything has been processed (no CTRL-C happened):
            next(stream)
        except StopIteration:
            sub_data["success"] = True
            sub_data["last_id"] = newest_id

        savedata.write()

        downloaded += stream.downloaded
        print()

    if not subs_in_cfg and not subs:
        LOG.warning("No subscription to sync, see configuration file: %r",
                    str(config.FILE))

    return downloaded
