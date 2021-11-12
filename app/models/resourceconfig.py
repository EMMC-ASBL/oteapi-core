"""
Pydantic ResourceConfig Data Model
"""

from typing import Dict, Optional

from pydantic import AnyUrl, BaseModel, Field


class ResourceConfig(BaseModel):
    """Resource Configuration for Dataset Distributions"""

    downloadUrl: Optional[AnyUrl] = Field(
        None,
        description=(
            "Definition: The URL of the downloadable file in a given format. E.g. CSV "
            "file or RDF file. The format is indicated by the distribution's "
            "`dct:format` and/or `dcat:mediaType`.\n\nUsage: `dcat:downloadURL` "
            "*SHOULD* be used for the URL at which this distribution is available "
            "directly, typically through a HTTP Get request."
        ),
    )
    mediaType: Optional[str] = Field(
        None,
        description=(
            "The media type of the distribution as defined by IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]"
            ".\n\nUsage: This property *SHOULD* be used when the media"
            " type of the distribution is defined in IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]"
            ", otherwise `dct:format` *MAY* be used with different values."
        ),
    )
    accessUrl: Optional[AnyUrl] = Field(
        None,
        description=(
            "A URL of the resource that gives access to a distribution of "
            "the dataset. E.g. landing page, feed, SPARQL endpoint.\n\nUsage: "
            "`dcat:accessURL` *SHOULD* be used for the URL of a service or location "
            "that can provide access to this distribution, typically through a Web "
            "form, query or API call.\n`dcat:downloadURL` is preferred for direct "
            "links to downloadable resources.\nIf the distribution(s) are accessible "
            "only through a landing page (i.e. direct download URLs are not known), "
            "then the landing page URL associated with the `dcat:Dataset` *SHOULD* be "
            "duplicated as access URL on a distribution (see "
            "[§ 5.7 Dataset available only behind some Web page](https://www.w3.org/TR/vocab-dcat-2/#example-landing-page))."  # pylint: disable=line-too-long
        ),
    )
    accessService: Optional[str] = Field(
        None,
        description=(
            "A data service that gives access to the distribution of the "
            "dataset.\n\nUsage: `dcat:accessService` *SHOULD* be used to link to a "
            "description of a `dcat:DataService` that can provide access to this "
            "distribution."
        ),
    )
    license: Optional[str] = Field(
        None,
        description=(
            "A legal document under which the distribution is made available.\n\nUsage:"
            " Information about licenses and rights *SHOULD* be provided on the level "
            "of Distribution. Information about licenses and rights *MAY* be provided "
            "for a Dataset in addition to but not instead of the information provided "
            "for the Distributions of that Dataset. Providing license or rights "
            "information for a Dataset that is different from information provided for"
            " a Distribution of that Dataset *SHOULD* be avoided as this can create "
            "legal conflicts. See also guidance at "
            "[§ 8. License and rights statements](https://www.w3.org/TR/vocab-dcat-2/#license-rights)."  # pylint: disable=line-too-long
        ),
    )
    accessRights: Optional[str] = Field(
        None,
        description=(
            "A rights statement that concerns how the distribution is "
            "accessed.\n\nUsage: Information about licenses and rights *MAY* be "
            "provided for the Distribution. See also guidance at "
            "[§ 8. License and rights statements](https://www.w3.org/TR/vocab-dcat-2/#license-rights)."  # pylint: disable=line-too-long
        ),
    )
    description: Optional[str] = Field(
        None, description="A free-text account of the distribution."
    )
    published: Optional[str] = Field(None, description="")
    configuration: Optional[Dict] = Field(
        None,
        description="Resource-specific configuration options given as key/value-pairs.",
    )


class OTEUrl(BaseModel):
    """pydantic datamodel representing the AnyUrl type

    This class is useful when a strategy is created
    based on a field from AnyUrl, such as 'scheme' for
    download strategy
    """

    url: str
    scheme: str
    host: str
    tld: str
    host_type: str
    path: str
    query: str


def url_to_model(anyurl: AnyUrl) -> OTEUrl:
    """
    Convert the pydantic AnyUrl type to a OTEUrl datamodel
    """
    return OTEUrl(
        url=str(anyurl),
        scheme=anyurl.scheme,
        host=anyurl.host,
        tld=anyurl.tld,
        host_type=anyurl.host_type,
        path=anyurl.path,
        query=anyurl.path,
    )
