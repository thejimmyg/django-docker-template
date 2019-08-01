import django.core.mail.backends.smtp
import logging

logger = logging.getLogger(__name__)  # or you could enter a specific logger name
    
class LoggingBackend(django.core.mail.backends.smtp.EmailBackend):

    def send_messages(self, email_messages):
        try:
            for msg in email_messages:
                logger.error(u"Sending message '%s' to recipients: %s", msg.subject, msg.to)
        except:
            logger.exception("Problem logging recipients, ignoring")
   
        return super(LoggingBackend, self).send_messages(email_messages)
