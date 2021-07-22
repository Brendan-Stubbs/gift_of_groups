var ideaModalDoesExist = false;
var relationModalDoesExist = false;

function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function getFormData(object) {
  const formData = new FormData();
  Object.keys(object).forEach((key) => formData.append(key, object[key]));
  return formData;
}

function vote_for_gift_ajax(idea_id) {
  let data = {
    id: idea_id,
  };

  $.ajax({
    type: "GET",
    url: "/ajax/vote_for_gift/" + idea_id + "/",
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    success: function (resp) {
      update_votes(resp, idea_id);
    },
  });
}

function invite_to_gift_ajax(gift_id) {
  let data = new FormData(document.getElementById("non-group-form"));
  data.append("gift_id", gift_id);

  $.ajax({
    type: "POST",
    url: `/ajax/invite_to_gift/${gift_id}/`,
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    success: function (resp) {
      $("#invite_message").text(resp.message).show();
      $("#non-group-form").trigger("reset");
    },
  });
}

function update_votes(resp, idea_id) {
  $(`#vote_counter${idea_id}`).text(resp.total_votes);
  $(`#vote_button${idea_id}`)
    .removeClass("clickable white-text")
    .addClass("grey-text");
}

function getFormForExistingIdea(idea_id) {
  $.ajax({
    type: "GET",
    url: `/ajax/get_idea_form/${idea_id}`,
    beforeSend: function () {
      if (!ideaModalDoesExist) {
        const emptyIdeaModal = `<div id="ideaEditModal" class="modal"><div class="modal-content" id="ideaEditModalBody" center-align"></div></div>`;
        $("body").append(emptyIdeaModal);
        $("#ideaEditModal").modal();
        ideaModalDoesExist = true;
      }
      ideaModalBody = $("#ideaEditModalBody");
      ideaModalBody
        .empty()
        .append(
          `<div style="text-align: center"><h4">We are hard at work fetching your form, please be patient</h4><br><br><br><i style="font-size: 60px" class="fas fa-circle-notch fa-spin"></i></div>`
        );
      $("#ideaEditModal").modal("open");
    },
    success: function (resp) {
      $("#ideaEditModalBody").empty().append(resp.rendered_form);
      $("#edit_idea_form").submit(function (event) {
        event.preventDefault();
      });
    },
    error: function (resp) {
      alert(
        "There was an error fetching the form, please try again. If the problem persists please try refreshing the page"
      );
    },
  });
}

function getFormForExistingRelation(relation_id) {
  $.ajax({
    type: "GET",
    url: `/ajax/get_relation_form/${relation_id}`,
    beforeSend: function () {
      if (!relationModalDoesExist) {
        const emptyIdeaModal = `<div id="relationEditModal" class="modal"><div class="modal-content" id="relationEditModalBody" center-align"></div></div>`;
        $("body").append(emptyIdeaModal);
        $("#relationEditModal").modal();
        relationModalDoesExist = true;
      }
      relationModalBody = $("#relationEditModalBody");
      relationModalBody
        .empty()
        .append(
          `<div style="text-align: center"><h4">We are hard at work fetching your form, please be patient</h4><br><br><br><i style="font-size: 60px" class="fas fa-circle-notch fa-spin"></i></div>`
        );
      $("#relationEditModal").modal("open");
    },
    success: function (resp) {
      $("#relationEditModalBody").empty().append(resp.rendered_form);
      $("select").formSelect();
      $("#edit_relation_form").submit(function (event) {
        event.preventDefault();
      });
    },
    error: function (resp) {
      alert(
        "There was an error fetching the form, please try again. If the problem persists please try refreshing the page"
      );
    },
  });
}

function showBirthdayCardPromptModal(firstName, giftId) {
  const promptString = `You are about to generate a birthday card for ${firstName} \nThis will make a link available to you, which you can then share with the lucky receiver of the gift`;
  if (confirm(promptString)) {
    createBirthdayCard(giftId);
  }
}

function createBirthdayCard(giftId) {
  $.ajax({
    type: "GET",
    url: `/ajax/generate_card/${giftId}/`,
    success: (resp) => {
      window.location = resp.link;
    },
    error: () => alert("There was an error, please try again"),
  });
}

function add_suggestion_ajax(gift_id, user_id, idea_id = undefined) {
  $("#suggestion-messages").text("");
  let data = new FormData(document.getElementById("suggestionForm"));
  data.append("user_id", user_id);
  data.append("gift_id", gift_id);
  $.ajax({
    type: "POST",
    url: "/ajax/add_gift_suggestion/",
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    success: function (resp) {
      $("#giftSuggestions").empty().append(resp.gift_suggestion_component);
      $("#suggestion-messages").attr("class", "green-text").text(resp.message);
      $("input", "#suggestionForm").val("");
      $("textarea", "#suggestionForm").val("");
    },
    error: function (resp) {
      alert(resp.message);
      $("#suggestion-messages")
        .attr("class", "red-text")
        .text("There was an error please ensure you are logged in");
    },
  });
}

function updateSuggestion(idea_id) {
  let data = new FormData($("#edit_idea_form")[0]);

  $.ajax({
    type: "POST",
    url: `/ajax/update_idea/${idea_id}`,
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    success: function (resp) {
      $("#giftSuggestions").empty().append(resp.gift_suggestion_component);
      $("#ideaEditModal").modal("close");
    },
    error: function (resp) {
      alert(
        "There was an error saving your changes, please refresh the page and try again"
      );
    },
  });
}

function updateRelation(relation_id) {
  let data = new FormData($("#edit_relation_form")[0]);
  const payment_has_cleared = $("#payment_has_cleared_edit").is(":checked");
  data.append("payment_has_cleared", payment_has_cleared);

  $.ajax({
    type: "POST",
    url: `/ajax/captain_update_relation/${relation_id}`,
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    success: function (resp) {
      $("#relationEditModal").modal("close");
      location.reload();
    },
    error: function (resp) {
      alert(
        "There was an error saving your changes, please refresh the page and try again"
      );
    },
  });
}

function clearForm(form_id) {
  $("input", "#suggestionForm").val("");
  $("textarea", "#suggestionForm").val("");
}

function mark_gift_complete(gift_id) {
  window.location.replace(`/mark_gift_complete/${gift_id}`);
}

function mark_as_paid() {
  $("#id_has_made_payment").prop("checked", true).trigger("change");
}

function ajax_update_user_gift_form(gift_relation_id) {
  $("#user_gift_detail_success").attr("class", "hidden-message green-text");
  let data = new FormData(document.getElementById("user_gift_detail_form"));
  data.append("gift_relation_id", gift_relation_id);
  const changeableValues = [
    "receiver_message",
    "participation_status",
    "contribution",
  ];

  $.ajax({
    type: "POST",
    url: `/ajax/update_user_gift_relation/`,
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    beforeSend: function () {
      changeableValues.forEach((item) => {
        $(`#${item}_spinner`)
          .removeClass("fas fa-check")
          .addClass("fas fa-circle-notch fa-spin")
          .css("display", "inline-block");
      });
    },
    success: function (resp) {
      $("#user_gift_detail_success").removeClass("hidden-message");
      $("#target-details").empty().append(resp.gift_progress_component);

      changeableValues.forEach((item) => {
        if (resp[item]) {
          $(`#${item}_spinner`)
            .removeClass("fas fa-circle-notch fa-spin")
            .addClass("fas fa-check")
            .css("display", "inline-block");
        } else {
          $(`#${item}_spinner`)
            .removeClass("fas fa-check")
            .addClass("fas fa-circle-notch fa-spin")
            .css("display", "none");
        }
      });

      if (resp.has_made_payment) {
        $("#notify-button").attr("disabled", true);
      }
    },
    error: function (resp) {
      alert(
        "There was an error saving your changes, please refresh the page and try again"
      );
    },
  });
}

function ajax_post_comment(gift_id) {
  let data = new FormData(document.getElementById("comment_form"));
  data.append("gift_id", gift_id);
  $.ajax({
    type: "POST",
    url: `/ajax/post_gift_comment/${gift_id}/`,
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    beforeSend: function () {
      $("#id_content").val("");
      $("#comments-refresh").hide();
      $("#comments-loading").show();
    },
    success: function (resp) {
      $("#comment_list").empty().append(resp.comments_component);
      $("#comments-loading").hide();
      $("#comments-refresh").show();
    },
    error: function (resp) {
      alert(
        "There was an error posting you comment, please refresh the page or try again later"
      );
    },
  });
}

function refresh_comments(gift_id) {
  $.ajax({
    type: "GET",
    url: `/ajax/get_comments/${gift_id}/`,
    beforeSend: function () {
      $("#comments-refresh").hide();
      $("#comments-loading").show();
    },
    complete: setTimeout(function () {
      $("#comments-loading").hide();
      $("#comments-refresh").show();
    }, 1000),
    success: function (resp) {
      $("#comment_list").empty().append(resp.comments_component);
    },
  });
}

function ajax_confirm_payment(relation_id) {
  $.ajax({
    type: "GET",
    url: `/ajax/captain_confirm_payment/${relation_id}/`,
    success: function (resp) {
      $("#captain_management_component")
        .empty()
        .append(resp.captain_management_component);
      $("#target-details").empty().append(resp.gift_progress_component);
    },
  });
}

function ajax_update_email_notifications(relation_id) {
  let data = new FormData(document.getElementById("comment_form"));
  $.ajax({
    type: "POST",
    url: `/ajax/update_email_notifications/${relation_id}/`,
    dataType: "json",
    data: data,
    contentType: false,
    processData: false,
    enctype: "multipart/form-data",
    success: function (resp) {
      // do something
    },
  });
}

$(document).ready(function () {
  let invite_link = $("#inviteLink");

  $("select").formSelect();
  $("#suggestionForm").submit(function (event) {
    event.preventDefault();
  });
  $("#user_gift_detail_form").submit(function (event) {
    event.preventDefault();
  });
  $("#comment_form").submit(function (event) {
    event.preventDefault();
  });
  $("#non-group-form").submit(function (event) {
    event.preventDefault();
  });
  $("#inviteLinkBtn").click(function (event) {
    invite_link.css("display", "block");
    document.querySelector("#inviteLink").select();
    let copied = document.execCommand("copy");
    invite_link.css("display", "none");

    if (copied) {
      alert("Link copied to clipboard");
    }
  });
});
