"""Persistent image storage for member photos on serverless deployments."""

from __future__ import annotations

import os
import uuid
from pathlib import PurePath

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage


class CloudinaryMemberStorage(Storage):
    """Store member portraits in Cloudinary and persist a compact asset key."""

    folder = "akatsuki/members"

    def _open(self, name, mode="rb"):
        raise NotImplementedError("Cloudinary assets are served directly by their URL.")

    def _save(self, name, content):
        if not os.getenv("CLOUDINARY_URL"):
            raise ImproperlyConfigured(
                "Member photo uploads need the CLOUDINARY_URL environment variable."
            )

        cloudinary.config()
        key = uuid.uuid4().hex
        result = cloudinary.uploader.upload(
            content,
            folder=self.folder,
            public_id=key,
            overwrite=False,
            resource_type="image",
        )
        return f"{key}.{result['format']}"

    def delete(self, name):
        key, _ = self._asset_parts(name)
        cloudinary.uploader.destroy(
            f"{self.folder}/{key}", resource_type="image", invalidate=True
        )

    def exists(self, name):
        # Every upload gets a random public ID, so collisions are not possible.
        return False

    def url(self, name):
        key, image_format = self._asset_parts(name)
        public_id = f"{self.folder}/{key}"
        url, _ = cloudinary_url(public_id, format=image_format, secure=True)
        return url

    @staticmethod
    def _asset_parts(name):
        filename = PurePath(name).name
        key, extension = os.path.splitext(filename)
        if not key or not extension:
            raise ValueError("Invalid Cloudinary member photo key.")
        return key, extension.lstrip(".")
