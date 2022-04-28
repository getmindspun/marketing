""" Extra hubspot functionality """
import os
import typing

from tld import get_fld

from hubspot import HubSpot
from hubspot.crm import companies, contacts


class HubspotClient(HubSpot):
    """ Extented Hubspot client """

    def __init__(self):
        super().__init__(api_key=os.environ["HUBSPOT_API_KEY"])

    def get_company_by_domain(self, domain: str) -> typing.Optional[dict]:
        """ Find company by domain """
        domain_filter = companies.Filter(
            property_name="domain", operator="EQ", value=domain
        )
        filter_group = companies.FilterGroup(filters=[domain_filter])
        public_object_search_request = companies.PublicObjectSearchRequest(
            filter_groups=[filter_group],
            properties=[
                "domain", "website",
                "lighthouse_base_score", "lighthouse_optimized_score"
            ]
        )
        result = self.crm.companies.search_api.do_search(
            public_object_search_request=public_object_search_request
        )
        if result.results:
            return result.results[0]

        return None

    def create_company(self, url: str):
        """ Create a new company """
        domain = get_fld(url)

        simple_public_object_input = companies.SimplePublicObjectInput(
            properties={"domain": domain, "website": url}
        )
        return self.crm.companies.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )

    def archive_company(self, company_id: str) -> None:
        """ Delete a company """
        self.crm.companies.basic_api.archive(company_id=company_id)

    def update_company_property(self, company_id: str, **kwargs) -> None:
        """ Update a company property """
        simple_public_object_input = companies.SimplePublicObjectInput(
            properties=kwargs
        )
        self.crm.companies.basic_api.update(
            company_id=company_id,
            simple_public_object_input=simple_public_object_input
        )

    def get_contact_by_email(self, email: str):
        """ Lookup a contact by email """
        email_filter = contacts.Filter(
            property_name="email", operator="EQ", value=email
        )
        filter_group = contacts.FilterGroup(filters=[email_filter])
        public_object_search_request = contacts.PublicObjectSearchRequest(
            filter_groups=[filter_group],
        )
        result = self.crm.contacts.search_api.do_search(
            public_object_search_request=public_object_search_request
        )
        if result.results:
            return result.results[0]

        return None

    def _associate_contact_to_company(
            self, contact_id: str, company_id: str
    ) -> None:
        self.crm.contacts.associations_api.create(
            contact_id=contact_id,
            to_object_type="company",
            to_object_id=company_id,
            association_type="contact_to_company"
        )

    def create_contact(self, email: str, company_id: str):
        """ Create a contact """

        simple_public_object_input = contacts.SimplePublicObjectInput(
            properties={"email": email}
        )
        contact = self.crm.contacts.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )

        self._associate_contact_to_company(contact.id, company_id)

        return contact

    def archive_contact(self, contact_id: str) -> None:
        """ Delete a company """
        self.crm.contacts.basic_api.archive(contact_id)
