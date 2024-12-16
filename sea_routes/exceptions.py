class RouteNotFoundException(Exception):
    def __init__(self, route_id: int):
        self.route_id = route_id
        self.message = f"No route with id {route_id} has been found. Try accessing different id or view the list of ids by using /routes endpoint."
        super().__init__(self.message)
