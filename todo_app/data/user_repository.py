from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def get_user_from_id(self, user_id):
        """
        Looks up user from store by id
        Args:
            user_id: The id of the user to lookup

        Returns: The user or None
        """
        raise NotImplementedError

    @abstractmethod
    def save_user(self, user):
        """
        Saves user in store
        Args:
            user: User to store

        Returns: None
        """
        raise NotImplementedError

    def set_user_roles(self, user_id, roles):
        """
        Sets roles for user with id of user_id
        Args:
            user_id: id of the user to set roles on
            roles: roles to set - these replace any existing roles

        Returns: None
        """
        raise NotImplementedError

    def does_user_have_role(self, user_id, role):
        """
        Checks if user has given role
        Args:
            user_id: id of user to check
            role: role to check

        Returns: Boolean with result of check
        """
        raise NotImplementedError
