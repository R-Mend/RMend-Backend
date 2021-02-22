from django.urls import path
from .views import AuthorityIssueTypeCreateView, AuthorityIssueTypeDeleteView, IssueTypeGroupView
from .views import AuthorityIssueTypeGroupView, AuthorityIssueTypeGroupCreateView, AuthorityIssueTypeGroupDeleteView


app_name = 'rmend_authorities'

urlpatterns = [
    path('issue-groups/', IssueTypeGroupView.as_view()),
    path('authority/<int:authority_id>/issue-groups', AuthorityIssueTypeGroupView.as_view()),
    path('authority/<int:authority_id>/issue-groups/create', AuthorityIssueTypeGroupCreateView.as_view()),
    path('authority/<int:authority_id>/issue-groups/delete', AuthorityIssueTypeGroupDeleteView.as_view()),
    path('authority/<int:authority_id>/issue-types/create', AuthorityIssueTypeCreateView.as_view()),
    path('authority/<int:authority_id>/issue-types/delete', AuthorityIssueTypeDeleteView.as_view())
]
