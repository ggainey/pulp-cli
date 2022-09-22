from typing import IO, Any, ClassVar

from pulpcore.cli.common.context import (
    EntityDefinition,
    PluginRequirement,
    PulpContentContext,
    PulpEntityContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
    registered_repository_contexts,
)
from pulpcore.cli.common.i18n import get_translation

translation = get_translation(__name__)
_ = translation.gettext


class PulpAnsibleCollectionVersionContext(PulpContentContext):
    ENTITY = _("ansible collection version")
    ENTITIES = _("ansible collection versions")
    HREF = "ansible_collection_version_href"
    ID_PREFIX = "content_ansible_collection_versions"
    UPLOAD_ID: ClassVar[str] = "upload_collection"

    def upload(self, file: IO[bytes]) -> Any:
        return self.call("upload", uploads={"file": file.read()})


class PulpAnsibleRoleContext(PulpContentContext):
    ENTITY = _("ansible role")
    ENTITIES = _("ansible roles")
    HREF = "ansible_role_href"
    ID_PREFIX = "content_ansible_roles"


class PulpAnsibleCollectionVersionSignatureContext(PulpContentContext):
    ENTITY = _("ansible collection version signature")
    ENTITIES = _("ansible collection version signatures")
    HREF = _("ansible_collection_version_signature_href")
    ID_PREFIX = "content_ansible_collection_signatures"


class PulpAnsibleDistributionContext(PulpEntityContext):
    ENTITY = _("ansible distribution")
    ENTITIES = _("ansible distributions")
    HREF = "ansible_ansible_distribution_href"
    ID_PREFIX = "distributions_ansible_ansible"

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial=partial)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpAnsibleRoleRemoteContext(PulpRemoteContext):
    ENTITY = _("role remote")
    ENTITIES = _("role remotes")
    HREF = "ansible_role_remote_href"
    ID_PREFIX = "remotes_ansible_role"


class PulpAnsibleCollectionRemoteContext(PulpRemoteContext):
    ENTITY = _("collection remote")
    ENTITIES = _("collection remotes")
    HREF = "ansible_collection_remote_href"
    ID_PREFIX = "remotes_ansible_collection"
    collection_nullable = ["auth_url", "requirements_file", "token"]

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial=partial)
        if "requirements" in body.keys():
            body["requirements_file"] = body.pop("requirements")
        return body


class PulpAnsibleRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "ansible_ansible_repository_version_href"
    ID_PREFIX = "repositories_ansible_ansible_versions"


class PulpAnsibleRepositoryContext(PulpRepositoryContext):
    HREF = "ansible_ansible_repository_href"
    ID_PREFIX = "repositories_ansible_ansible"
    ENTITY = _("ansible repository")
    ENTITIES = _("ansible repositories")
    VERSION_CONTEXT = PulpAnsibleRepositoryVersionContext
    CAPABILITIES = {"pulpexport": [PluginRequirement("ansible")]}
    NULLABLES = PulpRepositoryContext.NULLABLES | {"gpgkey"}


registered_repository_contexts["ansible:ansible"] = PulpAnsibleRepositoryContext
