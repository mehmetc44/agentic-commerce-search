from repositories.review_repository import ReviewRepository

class ReviewService:
    def __init__(self):
        self.repository = ReviewRepository()

    def get_product_reviews(self, product_id: int):
        return self.repository.get_by_product_id(product_id)
