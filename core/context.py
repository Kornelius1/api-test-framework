class TestContext:
    """Menyimpan data yang di-share antar test."""
    def __init__(self):
        self.token: str = None
        self.user_id: int = None
        self.business_id: int = None
        self.business_slug: str = None
        self.resource_type_id: int = None
        self.resource_id: int = None
        self.reservation_id: int = None
        self.google_channel_id: str = None

    def set_auth(self, token: str, user_id: int, business_id: int, business_slug: str):
        self.token = token
        self.user_id = user_id
        self.business_id = business_id
        self.business_slug = business_slug

    def set_resource_type(self, resource_type_id: int):
        self.resource_type_id = resource_type_id

    def set_resource(self, resource_id: int):
        self.resource_id = resource_id

    def set_reservation(self, reservation_id: int):
        self.reservation_id = reservation_id