# vim: set sw=4 ts=4 sts=4 noet:
import re
import email
from smtplib import SMTPRecipientsRefused

from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader

from amancay.models import Pending_Messages
from amancay.btsqueries import SoapQueries

def bug(request, bug_number=None):
    """
    Renders a bug page.

    If the given bug page has been reached as a result of a POST action, the
    data sent will be processed by process_bug_post and the bug will be
    rendered after that to the user.
    """
    # Process get
    if request.method == 'GET' and not bug_number:
        bug_number = request.GET['id'].strip()

    # Process post
    info = process_bug_post(request, bug_number)

    # FIXME: we need API
    request.user.subscribed = False
    queries = SoapQueries()
    try:
        b = re.sub('[a-zA-Z#]','', bug_number)
        bug_number = int(b)
        bug_status = queries.get_bugs_status(bug_number)[0]
    except (IndexError, ValueError):
            return render_to_response('search.html',
                              {'bug_number': bug_number,
                               'info_to_user': 'There is no bug with such number, please try again',
                               'bug_originator': '',
                               'bug_status': '',
                               'bug_messages': '',
                               'bug_is_fav': ''},
                              context_instance=RequestContext(request))
    bug_originator = email.Utils.parseaddr(bug_status['originator'])
    bug_log = queries.get_bug_log(bug_number)

    # having as a selected bug is not the same as subscribing
    if request.user.is_authenticated():
        bug_is_fav = bool(request.user.bug_set.filter(number=bug_number)[:1])
    else:
        bug_is_fav = bug_number in request.session.get('bug_set', [])

    # Regular expressions to parse the mails
    from_re = re.compile('^From: ?(.+)$', re.MULTILINE)
    subject_re = re.compile('^Subject: ?(.+)$', re.MULTILINE)
    date_re = re.compile('^Date: ?(.+)$', re.MULTILINE)

    bug_messages = []
    for item in bug_log:
        message = {}
        # Parse the header
        from_value = from_re.findall(item['header'])
        subject_value = subject_re.findall(item['header'])
        date_value = date_re.findall(item['header'])
        # Filter the value
        if from_value:
            e_from = email.Utils.parseaddr(from_value[0])
            d_from = email.Header.decode_header(e_from[0])
            if (d_from[0][1] != None):
                message['from'] = [d_from[0][0].decode(d_from[0][1]), e_from[1]]
            else:
                message['from'] = [e_from[0], e_from[1]]

            if not message['from'][0] and message['from'][1]:
                message['from'][0] = message['from'][1]

        if subject_value:
            message['subject'] = subject_value[0]

        if date_value:
            message['date'] = email.Utils.mktime_tz(email.Utils.parsedate_tz(
                                                     date_value[0]))

        # Get the body
        message['body'] = ''
        content = item['header'] + '\n' + item['body']
        content = email.message_from_string(content)
        if content.is_multipart():
            for part in content.walk():
                if (part.get_content_maintype() == 'multipart'):
                    continue
                if part['content-disposition'] and\
                   part['content-disposition'][:10] == 'attachment':
                    message['body'] += '[attach: %s]' % part.get_filename()
                else:
                    message['body'] += part.get_payload(decode=1) + '\n'
        else:
            message['body'] = content.get_payload(decode=1)

        bug_messages.append(message)

    return render_to_response('bug.html',
                              {'bug_number': bug_number,
                               'info_to_user': info,
                               'bug_originator': bug_originator,
                               'bug_status': bug_status,
                               'bug_messages': bug_messages,
                               'bug_is_fav': bug_is_fav},
                              context_instance=RequestContext(request))

def process_bug_post(request, bug_number):
    """
    Process the different forms based on presence of some fields.
    """
    form_type = request.POST.get('form_type', None)

    if not form_type:
        return None

    if form_type == 'comment':
        return add_comment(request, bug_number)
    elif form_type == 'reassign':
        return reassign(request, bug_number)
    elif form_type == 'retitle':
        return retitle(request, bug_number)
    elif form_type == 'close':
        return close(request, bug_number)
    elif form_type == 'severity':
        return severity(request, bug_number)
    elif form_type == 'owner':
        return change_owner(request, bug_number)
    else:
        return None

def change_owner(request, bug_number):
    new_owner_email = request.POST.get('new_owner_email')

    to_address = ['control@bugs.debian.org',
                    '%s@bugs.debian.org' % bug_number]
    text = 'owner %s %s' % (bug_number, new_owner_email)
    text += '\nthanks\n\n'

    subject = 'Changing owner of Debian Bug #%s to %s' % (bug_number, new_owner_email)

    return handle_email(request, to_address, subject, text)

def add_comment(request, bug_number):
    subject = request.POST.get('subject')
    comment = request.POST.get('comment')

    if subject and comment:
        to_address = ['%s@bugs.debian.org' % bug_number]
        # If the user is registered, we send the mail.  If not, we store it, and
        # validate the email
        return handle_email(request, to_address, subject, comment)
    else:
        return 'You need to enter both the subject and the comment.'

def reassign(request, bug_number):
    package = request.POST.get('reassign_to')
    version = request.POST.get('reassign_version')
    comment = request.POST.get('reassign_comment')

    if package:
        to_address = ['control@bugs.debian.org',
                      '%s@bugs.debian.org' % bug_number]
        text = 'reassign %s %s' % (bug_number, package)

        if version:
            text += ' %s' % version
        text += '\nthanks\n\n'

        if comment:
            text += comment
        subject = 'Reassigning Debian Bug #%s to Package %s' % (bug_number, package)

        return handle_email(request, to_address, subject, text)
    else:
        return None

def retitle(request, bug_number):
    new_title = request.POST.get('retitle_to')
    comment = request.POST.get('retitle_comment')

    if new_title:
        to_address = ['control@bugs.debian.org',
                      '%s@bugs.debian.org' % bug_number]
        text = 'retitle %s %s' % (bug_number, new_title)
        text += '\nthanks\n\n'

        if comment:
            text += comment
        subject = 'Retitling Debian Bug #%s ' % bug_number

        return handle_email(request, to_address, subject, text)
    else:
        return None

def close(request, bug_number):
    version = request.POST.get('close_version')
    comment = request.POST.get('close_comment')

    if version:
        to_address = ['%s-done@bugs.debian.org' % bug_number]
        text = 'Version: %s\n\n' % version

        if comment:
            text += comment
        subject = 'Closing Debian Bug #%s ' % bug_number

        return handle_email(request, to_address, subject, text)
    else:
        return None

def severity(request, bug_number):
    new_severity = request.POST.get('severity')
    comment = request.POST.get('severity_comment')

    if new_severity:
        to_address = ['control@bugs.debian.org',
                      '%s@bugs.debian.org' % bug_number ]
        text = 'severity %s %s' % (bug_number, new_severity)
        text += '\nthanks\n\n'

        if comment:
            text += comment
        subject = 'Changing Debian Bug #%s\'s severity to %s ' % (bug_number, new_severity)

        return handle_email(request, to_address, subject, text)
    else:
        return None

def handle_email(request, to_address, subject, text):
    """
    Sends an email to to_address if the user is authenticated, otherwise it
    saves it in queue.
    """
    if request.user.is_authenticated():
        send_mail(subject, text, request.user.email, to_address)
        return 'Your comment has been successfully sent'
    else:
        from_address = request.POST.get('from_email')
        pending_message(from_address, to_address, subject, text)
        return 'A mail has been sent to your address to validate it'

def pending_message(from_address, to_address, subject, comment):
    """
    Create a pending message and send the activation email.
    """
    import random, sha
    from django.contrib.sites.models import Site
    from django.conf import settings

    # Store the email in the pending message db
    salt = sha.new(str(random.random())).hexdigest()[:5]
    activation_key = sha.new(salt+subject+from_address).hexdigest()

    # Fix the to_address if necessary
    to_address = ','.join(to_address)

    # Prepare the message to send to the user
    message = Pending_Messages(from_address=from_address,
                to_address=to_address,
                subject=subject,
                comment=comment,
                digest=activation_key)
    message.save()
    message_template = loader.get_template('activate_comment.txt')
    message_context = Context({ 'activation_key': activation_key,
                                'subject': subject,
                                'text': comment,
                                'to_address': to_address,
                                'from_address': from_address,
                                'site_url': Site.objects.get_current().domain
                                })
    message = message_template.render(message_context)
    # Send the email to the user
    subject = 'Activate the bug actions you prepared at Amancay'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [from_address])

def activate_message(request, activation_key):
    """
    Flushes emails in the message queue corresponding to a given
    activation_key.
    """
    # Make sure the key we're trying conforms to the pattern of a
    # SHA1 hash; if it doesn't, no point even trying to look it up
    # in the DB.
    if re.match('[a-f0-9]{40}', activation_key):
        try:
            message = Pending_Messages.objects.filter(digest=activation_key)[0]
            to_address = message.to_address.split(',')
            send_mail(message.subject, message.comment, message.from_address, to_address)
            message.delete()
            status = 'Your message has now been successfully sent'
        except SMTPRecipientsRefused:
            status = 'Invalid destination: %s.' % message.to_address
        except IndexError:
            status = 'Invalid activation key'
    else:
        status = 'Malformed activation key'

    return render_to_response('search.html',
                              {'info_to_user': status},
                              context_instance=RequestContext(request))
