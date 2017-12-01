$(document).ready(function(){

	 // let $api_post_comments_list_url = $("#post_title_id").attr('data-api_post_comments_list_url');
  // let $post_comment_list = (api_post_comments_list_url) => {
  //   let $post_comments = $('#post_comments');
  //   console.log($api_post_comments_list_url);

  //   $.getJSON(api_post_comments_list_url, function(data) {   
  //     let comment_list = data.results
  //     let items = []
  //     if (comment_list == 0){
  //       $post_comments.html("<strong> No comments yet.</strong>");
  //     }
  //     else{
  //       $.each(comment_list, function(key, val){
  //         let timestamp = comment_list[key]['timestamp'];
  //         let updated = comment_list[key]['updated'];
  //         let content = comment_list[key]['content'];
  //         let user = comment_list[key]['user'];
  //         let replies = comment_list[key]['replies_count'];
  //         let comment_id = comment_list[key]['id'];
  //         let output = `<div class="card comment-card" data-comment_id="${comment_id}" id="comment_id_${comment_id}">
  //                   <div class="card-block">
  //                       <h5 class="card-title">By:${user}. <small class="text-muted">on: ${ timestamp }.  Replies: <span>${replies}</span></small></h6>
  //                       <p class="card-text" data-user="${ user }">${ content } </p>
  //                       <button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}">Reply</button> 
  //                       <button  class="btn btn-primary btn-sm button-view-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/posts/comments/${comment_id}/detail/">View Replies</button> 
  //                       <ul class="comment-replies mt-2">
  //                       </ul>
  //                   </div>
  //               </div>
  //           `;
  //         // output.appendTo($post_comments);
  //         items.push(output);
  //       });  
  //       $post_comments.html(items);
  //     }  
  //   });
  // };

  // $post_comment_list($api_post_comments_list_url);



// fetch post's comment list 
  let $api_post_detail_url = $("#post_title_id").attr('data-api_post_detail_url');
  let $post_single_comment = (api_post_detail_url) => {
    let $post_comments = $('#post_comments');
    let items = []

    $.getJSON(api_post_detail_url, function(data){
      let comment_list = data.comments;
      let comments_count = data.comment_count;
      let $post_comment_id = $('#post_comment_id');
      
      $post_comment_id.text(comments_count);

      if(comment_list.length === 0){
        $post_comments.html("<strong> No comments yet.</strong>");  
      }
      else{
        $.each(comment_list, function(key, val){
          if (comment_list[key].parent == null){
            let timestamp = comment_list[key]['timestamp'];
            let updated = comment_list[key]['updated'];
            let content = comment_list[key]['content'];
            let user = comment_list[key]['user'];
            let replies = comment_list[key]['replies_count'];
            let comment_id = comment_list[key]['id'];
            
            let output = `<div class="card comment-card" data-comment_id="${comment_id}" id="comment_id_${comment_id}">
                    <div class="card-block">
                        <h5 class="card-title">By:${user}. <small class="text-muted">on: ${ timestamp }.  Replies: <span>${replies}</span></small></h6>
                        <p class="card-text" data-user="${ user }">${ content } </p>
                        <button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}">Reply</button> 
                        <button  class="btn btn-primary btn-sm button-view-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/posts/comments/${comment_id}/detail/">View Replies</button> 
                        <ul class="comment-replies mt-2">
                        </ul>
                    </div>
                </div>
            `;
            items.push(output);         
          }  
        });
        $post_comments.html(items); // for single comment items[0]
      }
       
    });   
    // console.log(items)
    // return items;
  };

  console.log($api_post_detail_url);
  $post_single_comment($api_post_detail_url);




});